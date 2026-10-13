"""gate.py - the deterministic check that must PASS before a v3.3 run writes STATUS: DONE.

Why this exists
----------------
RUNBOOK_v3.md (C:\\Users\\User\\eda-routine\\RUNBOOK_v3.md) describes a signal engine with one hard line: SEARCH happens on
TRAIN (EXPLORE + the CONFIRM folds) as often as the run likes; VAL is only for CHECKING a candidate whose spec was frozen
before VAL was opened; TEST is never opened by the routine. Prose is advisory - an unattended run can write a plausible
REPORT.md without any of that having happened. This module makes the structural half CHECKED rather than trusted: it reads
the run folder's own files and refuses to pass if what they claim is inconsistent.

It knows: whether the required files exist; whether a rule file predates its result; whether every BELIEFS.md entry and
every candidates/F<n>.md spec carries its required fields; whether each posterior is its prior times the capped
weight_applied chain; whether a DROPPED hypothesis met the effort floor; whether every search result answers its leads; whether a search cell stayed off VAL; whether a candidate's spec
file existed before its CONFIRM and VAL cells, and is byte-for-byte the spec the VAL cell checked (sha256); whether VAL was
only opened for a candidate that held on the CONFIRM folds; whether every VAL pass is handed to the user in
TEST_REQUESTS.md; whether K (search looks and VAL checks, counted separately) is carried into MEMORY/LEDGER.md; and whether
STOP_REASON.md's claim matches all of that.

What it CANNOT enforce - stated plainly
----------------------------------------
- That a search cell's code did not read VAL rows (the load guard and the judge cover that).
- That `variants:` honestly counts every spec a search cell evaluated.
- That a new candidate after a VAL failure was found on TRAIN rather than shaped by what VAL showed.
- Anything about statistical correctness inside a cell's code.
These need the post-run judge agent (.claude/agents/eda-v3-judge.md). gate.py is the floor, not the ceiling.

Usage
-----
    python gate.py <run_dir> [--memory <MEMORY dir>]     (default MEMORY dir: <eda-routine>/MEMORY)

Exits 0 and prints PASS if every check passes. Exits 1 and prints FAIL plus every issue, numbered, if not. Runs recorded
before v3.3 (2026-10-13) used the older format and are not expected to pass this version.
"""
from __future__ import annotations

import glob
import hashlib
import os
import re
import sys
from dataclasses import dataclass, field


HYPOTHESIS_STATES = {"OPEN", "DROPPED", "CHECKED"}
BELIEF_REQUIRED_KEYS = ["parent", "source", "question", "hypothesis", "forbids", "rivals", "born_on",
                        "prior", "anchor", "posterior", "state"]
CANDIDATE_REQUIRED_KEYS = ["hypothesis", "variant_of", "spec", "construction", "pass_rule", "min_useful", "cost_line"]
SIGNAL_LABELS = {"STANDALONE", "COMBINE-ONLY"}   # set by the cost line; cost never decides a branch
STOP_REQUIRED_KEYS = ["rule", "open_count", "dropped_count", "frozen_count", "val_pass_count", "minutes", "detail"]
STOP_RULES = ("S1", "S2", "S3")
CELL_KINDS = {"search", "confirm", "val"}
BRANCHES = {"supported", "refuted", "inconclusive"}

MIN_CONFIRM_FOLDS = 2
MIN_SUPPORTED_FOLDS = 2   # a frozen candidate is CONFIRM-SHOWN with this many supported folds and none refuted
DRY_STREAK = 8            # S2: this many search cells in a row with no new candidate frozen
S1_MIN_CELLS, S1_MIN_MINUTES = 20, 90     # S1 ("nothing open") may not fire before either floor
S3_CELLS, S3_MINUTES = 60, 180            # S3 hard cap
MIN_SEARCH_BEFORE_DROP = 3                # search cells a hypothesis needs before it may be DROPPED

# Belief updating: posterior odds = prior odds x every weight_applied. A search cell looked at data the run may already
# have searched, so one search cell moves the odds at most 3x; a confirm or VAL check of a frozen spec at most 10x.
WEIGHT_CAP = {"search": 3.0, "confirm": 10.0, "val": 10.0}
POSTERIOR_TOLERANCE = 0.01  # absolute, on the probability scale (BELIEFS.md rounds to 2-3 places)

# Files every completed session must have, independent of how many hypotheses or cells it ran.
REQUIRED_FILES = [
    "DATA_CARD.md",
    "DATA_PROFILE.md",
    "OBSERVATIONS.md",
    "SPLITS.md",
    "BELIEFS.md",
    "ATTEMPTS.md",
    "DECISIONS.md",
    "ACCESS_LOG.md",
    "STOP_REASON.md",
    "REPORT.md",
]

# DATA_PROFILE.md must have a heading for each of these (RUNBOOK_v3.md PHASE 0, items 1-7).
DATA_PROFILE_SECTIONS = [1, 2, 3, 4, 5, 6, 7]


@dataclass
class Issue:
    code: str
    message: str


@dataclass
class GateReport:
    run_dir: str
    issues: list = field(default_factory=list)

    def add(self, code: str, message: str) -> None:
        self.issues.append(Issue(code, message))

    @property
    def ok(self) -> bool:
        return not self.issues


@dataclass
class Cell:
    nn: int
    hypothesis: str
    slice: str
    kind: str
    candidate: str | None = None
    spec_sha256: str | None = None
    method: str | None = None    # optional `method: M<n>` header (METHOD_SPEC.md id)
    controls: str | None = None  # search cells: the rival this look controls for (`none` if it controls none)
    conditional: str | None = None   # search cells: the regime / conditional split this look uses (`none` if none)
    rule_mtime: float = 0.0
    branch: str | None = None
    weight: float | None = None
    suggests: str | None = None
    variants: int = 1
    folds: dict = field(default_factory=dict)   # confirm cells: {fold: branch}


@dataclass
class Candidate:
    fid: str
    path: str
    fields: dict
    sha256: str
    mtime: float


# ------------------------------------------------------------------ file helpers

def _path(run_dir: str, *parts: str) -> str:
    return os.path.join(run_dir, *parts)


def _read(run_dir: str, *parts: str):
    p = _path(run_dir, *parts)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def _parse_kv_file(text: str, keys: list[str]) -> dict:
    """First `key: value` line for each wanted key, anywhere in the file."""
    out = {}
    for line in text.splitlines():
        m = re.match(r"^([a-z_0-9]+):\s*(.*)$", line.strip())
        if m and m.group(1) in keys and m.group(1) not in out:
            out[m.group(1)] = m.group(2).strip()
    return out


def _odds(p: float) -> float:
    return p / (1.0 - p)


def _prob(odds: float) -> float:
    return odds / (1.0 + odds)


def _given(v: str | None) -> bool:
    return bool(v) and v.strip().lower() not in ("none", "-", "no")


def sha256_of(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


# ------------------------------------------------------------------ individual checks

def check_required_files(run_dir: str, report: GateReport) -> None:
    for name in REQUIRED_FILES:
        if not os.path.exists(_path(run_dir, name)):
            report.add("missing_file", f"{name} does not exist in {run_dir}")


def check_data_profile_sections(run_dir: str, report: GateReport) -> None:
    text = _read(run_dir, "DATA_PROFILE.md")
    if text is None:
        return  # already reported by check_required_files
    found = set()
    for line in text.splitlines():
        m = re.match(r"^#{1,6}\s*(\d+)[.\)]", line.strip())
        if m:
            found.add(int(m.group(1)))
    missing = [n for n in DATA_PROFILE_SECTIONS if n not in found]
    if missing:
        report.add(
            "data_profile_incomplete",
            f"DATA_PROFILE.md is missing numbered section(s) {missing} "
            f"(PHASE 0 requires headings 1-7)",
        )


def check_splits(run_dir: str, report: GateReport) -> list[str]:
    """Parse SPLITS.md's `slices:` block. Returns the CONFIRM fold names in order (C1, C2, ...),
    or [] if the block is missing or malformed (reported)."""
    text = _read(run_dir, "SPLITS.md")
    if text is None:
        return []
    rows = re.findall(
        r"(?m)^\s*-\s*(EXPLORE|C\d+|VAL)\s+(\d{4}-\d{2}-\d{2})\s+(\d{4}-\d{2}-\d{2})\s*$", text
    )
    if not rows:
        report.add(
            "splits_no_block",
            "SPLITS.md has no machine-readable `slices:` block (`- <EXPLORE|C<j>|VAL> <from> <to>` lines)",
        )
        return []
    names = [r[0] for r in rows]
    folds = [n for n in names if n.startswith("C")]
    expected = ["EXPLORE"] + [f"C{i}" for i in range(1, len(folds) + 1)] + ["VAL"]
    if names != expected:
        report.add(
            "splits_bad_order",
            f"SPLITS.md slices are {names}; expected EXPLORE, C1..Cn in order, then VAL",
        )
    if len(folds) < MIN_CONFIRM_FOLDS:
        report.add(
            "splits_too_few_folds",
            f"SPLITS.md declares {len(folds)} CONFIRM fold(s); at least {MIN_CONFIRM_FOLDS} are required",
        )
    prev_to = None
    for name, start, end in rows:
        if start >= end:
            report.add("splits_bad_range", f"SPLITS.md {name}: from {start} is not before to {end}")
        if prev_to is not None and start < prev_to:
            report.add("splits_overlap", f"SPLITS.md {name} starts {start}, before the previous slice ends {prev_to}")
        prev_to = end
    return folds


def _parse_belief_blocks(text: str) -> list[dict]:
    """Split BELIEFS.md on '## H<n>' headings; one dict per block, lowercase keys -> first value."""
    blocks = re.split(r"(?m)^##\s*(H\d+)\b", text)
    out = []
    for i in range(1, len(blocks), 2):
        hid, body = blocks[i], blocks[i + 1]
        entry = {"_id": hid, "_raw": body}
        for line in body.splitlines():
            m = re.match(r"^([a-z_]+):\s*(.*)$", line.strip())
            if m and m.group(1) not in entry:
                entry[m.group(1)] = m.group(2).strip()
        out.append(entry)
    return out


def _born_slice(entry: dict) -> str:
    return entry.get("born_on", "").split()[0] if entry.get("born_on") else ""


def check_beliefs_format(run_dir: str, folds: list[str], report: GateReport) -> list[dict]:
    text = _read(run_dir, "BELIEFS.md")
    if text is None:
        return []
    entries = _parse_belief_blocks(text)
    if not entries:
        report.add("beliefs_empty", "BELIEFS.md has no '## H<n>' entries")
        return []
    valid_born = {"SOURCE", "EXPLORE"} | set(folds)
    valid = []
    for e in entries:
        missing = [k for k in BELIEF_REQUIRED_KEYS if not e.get(k)]
        if missing:
            report.add("beliefs_missing_fields", f"{e['_id']}: missing or empty field(s) {missing}")
            continue
        ok = True
        if e["forbids"].lower().startswith("none") and "no-story" not in e["forbids"].lower():
            report.add(
                "beliefs_no_forbid",
                f"{e['_id']}: 'forbids' is empty of content but not marked NO-STORY "
                f"('forbids: none - NO-STORY' is the only accepted empty form)",
            )
        for numeric_key in ("prior", "posterior"):
            try:
                v = float(e[numeric_key])
                if not (0.0 < v < 1.0):
                    raise ValueError
                e[numeric_key] = v
            except ValueError:
                ok = False
                report.add("beliefs_bad_number",
                           f"{e['_id']}: {numeric_key}='{e[numeric_key]}' is not a probability strictly between 0 and 1")
        if e["state"] not in HYPOTHESIS_STATES:
            ok = False
            report.add(
                "beliefs_bad_state",
                f"{e['_id']}: state='{e['state']}' is not one of {sorted(HYPOTHESIS_STATES)}",
            )
        if e["parent"].lower() != "none" and not re.match(r"^H\d+$", e["parent"]):
            report.add("beliefs_bad_parent", f"{e['_id']}: parent='{e['parent']}' is neither 'none' nor an H<n> id")
        if folds and _born_slice(e) not in valid_born:
            report.add(
                "beliefs_bad_born_on",
                f"{e['_id']}: born_on='{e['born_on']}' must start with SOURCE, EXPLORE or a declared fold {folds} "
                f"(never VAL: nothing is born on VAL)",
            )
        if ok:
            valid.append(e)
    ids = {e["_id"] for e in entries}
    for e in entries:
        if e.get("parent", "none").lower() != "none" and e["parent"] not in ids:
            report.add("beliefs_dangling_parent", f"{e['_id']}: parent '{e['parent']}' does not match any entry in this file")
    return valid


def check_candidates(run_dir: str, beliefs: list[dict], report: GateReport) -> dict:
    """candidates/F<n>.md: the frozen spec of every candidate that goes to CONFIRM and VAL."""
    ids = {e["_id"] for e in beliefs}
    out = {}
    for p in sorted(glob.glob(_path(run_dir, "candidates", "F*.md"))):
        m = re.search(r"(F\d+)\.md$", p)
        if not m:
            continue
        fid = m.group(1)
        with open(p, encoding="utf-8") as fh:
            kv = _parse_kv_file(fh.read(), CANDIDATE_REQUIRED_KEYS)
        missing = [k for k in CANDIDATE_REQUIRED_KEYS if not kv.get(k)]
        if missing:
            report.add("candidate_missing_fields", f"candidates/{fid}.md: missing or empty field(s) {missing}")
        if kv.get("hypothesis") and kv["hypothesis"] not in ids:
            report.add("candidate_unknown_hypothesis", f"candidates/{fid}.md: hypothesis '{kv['hypothesis']}' is not in BELIEFS.md")
        out[fid] = Candidate(fid, p, kv, sha256_of(p), os.path.getmtime(p))
    for c in out.values():
        v = c.fields.get("variant_of", "none")
        if v.lower() != "none" and v not in out:
            report.add("candidate_bad_variant_of", f"candidates/{c.fid}.md: variant_of '{v}' is not a candidate in this run")
    return out


def _parse_folds(raw: str) -> dict:
    return {k.strip(): v.strip() for k, v in re.findall(r"(C\d+)\s*=\s*([a-z]+)", raw or "")}


def check_cells(run_dir: str, folds: list[str], report: GateReport) -> list[Cell]:
    """Rule-before-result ordering and the headers of every rule and result file. Returns parsed cells, by number."""
    rule_files = sorted(glob.glob(_path(run_dir, "cells", "cell_*_rule.md")))
    if not rule_files:
        report.add("no_cells", "no cells/cell_*_rule.md found - PHASE 2 produced no cells")
        return []
    cells = []
    for rule_path in rule_files:
        m = re.search(r"cell_(\d+)_rule\.md$", rule_path)
        if not m:
            continue
        nn = m.group(1)
        result_path = _path(run_dir, "cells", f"cell_{nn}_result.md")
        if not os.path.exists(_path(run_dir, "cells", f"cell_{nn}_announce.md")):
            report.add("cell_missing_announce", f"cell_{nn}: no cell_{nn}_announce.md")

        with open(rule_path, encoding="utf-8") as fh:
            head = _parse_kv_file(fh.read(), ["hypothesis", "slice", "kind", "candidate", "spec_sha256", "method",
                                              "controls", "conditional"])
        missing = [k for k in ("hypothesis", "slice", "kind") if not head.get(k)]
        if missing:
            report.add(
                "cell_rule_no_header",
                f"cell_{nn}: rule.md lacks header line(s) {missing} (hypothesis / slice / kind: <search|confirm|val>)",
            )
            continue
        if head["kind"] not in CELL_KINDS:
            report.add("cell_bad_kind", f"cell_{nn}: kind='{head['kind']}' is not one of {sorted(CELL_KINDS)}")
            continue
        cell = Cell(int(nn), head["hypothesis"], head["slice"], head["kind"],
                    candidate=head.get("candidate") or None, spec_sha256=head.get("spec_sha256") or None,
                    method=head.get("method") or None, controls=head.get("controls") or None,
                    conditional=head.get("conditional") or None, rule_mtime=os.path.getmtime(rule_path))

        if not os.path.exists(result_path):
            report.add("cell_missing_result", f"cell_{nn}: no cell_{nn}_result.md")
            cells.append(cell)
            continue
        if os.path.getmtime(result_path) < cell.rule_mtime:
            report.add(
                "cell_result_before_rule",
                f"cell_{nn}: result.md is older than rule.md - the rule was not written first, "
                f"or the rule file was edited after the result existed",
            )
        with open(result_path, encoding="utf-8") as fh:
            res = _parse_kv_file(fh.read(), ["branch", "variants", "folds", "weight_applied", "suggests"])
        try:
            cell.weight = float(res.get("weight_applied", ""))
        except ValueError:
            report.add("cell_result_no_weight", f"cell_{nn}: result.md has no numeric 'weight_applied:' line")
        if cell.kind == "search":
            try:
                cell.variants = int(res.get("variants", ""))
                if cell.variants < 1:
                    raise ValueError
            except ValueError:
                report.add("cell_result_no_variants",
                           f"cell_{nn}: a search result needs `variants: <n >= 1>` (every spec it evaluated counts in K)")
            cell.suggests = res.get("suggests") or None
            if not cell.suggests:
                report.add("cell_result_no_suggests",
                           f"cell_{nn}: a search result needs a `suggests:` line - each lead -> H<n>, or "
                           f"`not pursued: <reason>`, or `none`")
        elif cell.kind == "confirm":
            cell.folds = _parse_folds(res.get("folds", ""))
            bad = {f: b for f, b in cell.folds.items() if b not in BRANCHES}
            if set(cell.folds) != set(folds) or bad:
                report.add("cell_result_bad_folds",
                           f"cell_{nn}: a confirm result needs `folds: C1=<branch>, ...` naming every declared fold "
                           f"{folds} with a branch in {sorted(BRANCHES)}")
        else:
            if res.get("branch") not in BRANCHES:
                report.add("cell_result_no_branch",
                           f"cell_{nn}: a val result needs a `branch:` line (one of {sorted(BRANCHES)})")
            else:
                cell.branch = res["branch"]
        cells.append(cell)
    return sorted(cells, key=lambda c: c.nn)


def confirm_shown(cell: Cell) -> bool:
    branches = list(cell.folds.values())
    return branches.count("supported") >= MIN_SUPPORTED_FOLDS and branches.count("refuted") == 0


def check_flow(run_dir: str, beliefs: list[dict], cands: dict, cells: list[Cell], folds: list[str],
               report: GateReport) -> dict:
    """Search stays on TRAIN; CONFIRM and VAL check frozen specs; VAL only after CONFIRM; every VAL pass goes to the user.
    Returns {candidate id: status}, status in FROZEN, CONFIRM-FAIL, CONFIRM-SHOWN, VAL-PASS, VAL-FAIL."""
    by_id = {e["_id"]: e for e in beliefs}
    train = {"EXPLORE", "TRAIN", "CONFIRM"} | set(folds)
    confirmed: dict = {}     # fid -> confirm cell
    valed: dict = {}         # fid -> val cell

    for c in cells:
        tag = f"cell_{c.nn:02d} ({c.hypothesis}, {c.slice}, {c.kind})"
        if c.hypothesis not in by_id:
            report.add("cell_unknown_hypothesis", f"{tag}: {c.hypothesis} is not an entry in BELIEFS.md")
            continue
        if c.kind == "search":
            sl = {s.strip() for s in c.slice.split(",")}
            if "VAL" in sl:
                report.add("search_on_val", f"{tag}: searching is TRAIN-only; VAL may only be opened by a kind: val cell")
            elif not sl <= train:
                report.add("cell_unknown_slice", f"{tag}: slice must be EXPLORE, a declared fold, CONFIRM or TRAIN")
            if c.candidate:
                report.add("search_names_candidate", f"{tag}: a search cell does not check a candidate; drop `candidate:`")
            continue

        cand = cands.get(c.candidate or "")
        if cand is None:
            report.add("check_no_candidate",
                       f"{tag}: a {c.kind} cell must name a frozen spec, `candidate: F<n>` with candidates/F<n>.md")
            continue
        if cand.fields.get("hypothesis") != c.hypothesis:
            report.add("check_wrong_hypothesis", f"{tag}: {cand.fid} belongs to {cand.fields.get('hypothesis')}")
        if cand.mtime > c.rule_mtime:
            report.add("check_spec_not_frozen",
                       f"{tag}: candidates/{cand.fid}.md is newer than this cell's rule - the spec was written or edited "
                       f"after the check was set up")

        if c.kind == "confirm":
            if c.slice != "CONFIRM":
                report.add("confirm_wrong_slice", f"{tag}: a confirm cell runs the frozen spec on every fold: slice: CONFIRM")
            if cand.fid in confirmed:
                report.add("confirm_twice",
                           f"{tag}: {cand.fid} already has a confirm cell; a changed spec is a new candidate (variant_of)")
            confirmed.setdefault(cand.fid, c)
        else:  # val
            if c.slice != "VAL":
                report.add("val_wrong_slice", f"{tag}: a kind: val cell must have slice: VAL")
            prior_confirm = confirmed.get(cand.fid)
            if prior_confirm is None or not confirm_shown(prior_confirm):
                report.add("val_not_confirm_shown",
                           f"{tag}: VAL is only for a candidate CONFIRM-SHOWN by an earlier confirm cell "
                           f"(>= {MIN_SUPPORTED_FOLDS} supported folds, none refuted)")
            if c.spec_sha256 != cand.sha256:
                report.add("val_spec_mismatch",
                           f"{tag}: spec_sha256 {c.spec_sha256} is not the sha256 of candidates/{cand.fid}.md ({cand.sha256}) "
                           f"- the spec changed after its VAL check, or the header is missing")
            if cand.fid in valed:
                report.add("val_twice",
                           f"{tag}: {cand.fid} was already checked on VAL; a changed spec is a new candidate (variant_of)")
            valed.setdefault(cand.fid, c)

    status = {}
    for fid in cands:
        if fid in valed:
            status[fid] = "VAL-PASS" if valed[fid].branch == "supported" else "VAL-FAIL"
        elif fid in confirmed:
            status[fid] = "CONFIRM-SHOWN" if confirm_shown(confirmed[fid]) else "CONFIRM-FAIL"
        else:
            status[fid] = "FROZEN"
    for fid, st in status.items():
        if st == "FROZEN":
            report.add("confirm_owed", f"{fid} was frozen but never run on the CONFIRM folds")
        if st == "CONFIRM-SHOWN":
            report.add("val_owed", f"{fid} is CONFIRM-SHOWN at the end of the session but was not checked on VAL")

    for e in beliefs:
        mine = [f for f, cd in cands.items() if cd.fields.get("hypothesis") == e["_id"]]
        if e["state"] == "CHECKED" and not any(status[f] in ("VAL-PASS", "VAL-FAIL") for f in mine):
            report.add("state_mismatch", f"{e['_id']}: CHECKED needs at least one of its candidates checked on VAL")

    passes = [f for f, st in status.items() if st == "VAL-PASS"]
    text = _read(run_dir, "TEST_REQUESTS.md") or ""
    blocks = re.split(r"(?m)^##\s*(F\d+)\b", text)
    listed = {blocks[i]: _parse_kv_file(blocks[i + 1], ["spec_sha256", "label"]) for i in range(1, len(blocks), 2)}
    for f in passes:
        if f not in listed:
            report.add("test_request_missing", f"{f} passed VAL but TEST_REQUESTS.md has no `## {f}` block for the user")
        elif listed[f].get("spec_sha256") != cands[f].sha256:
            report.add("test_request_bad_sha", f"TEST_REQUESTS.md {f}: spec_sha256 does not match candidates/{f}.md")
        if f in listed and listed[f].get("label", "").upper() not in SIGNAL_LABELS:
            report.add("test_request_no_label",
                       f"TEST_REQUESTS.md {f}: `label:` must be one of {sorted(SIGNAL_LABELS)} (from its cost line)")
    return status


def check_posteriors(beliefs: list[dict], cells: list[Cell], report: GateReport) -> None:
    """Every posterior = prior x the weight_applied of every cell on that hypothesis, each within its kind's cap."""
    for e in beliefs:
        mine = [c for c in cells if c.hypothesis == e["_id"]]
        odds, chain_ok = _odds(e["prior"]), True
        for c in mine:
            if c.weight is None:
                chain_ok = False
                continue
            cap = WEIGHT_CAP[c.kind]
            if not (1.0 / cap - 1e-9 <= c.weight <= cap + 1e-9):
                report.add("weight_over_cap",
                           f"cell_{c.nn:02d}: weight_applied {c.weight} is outside the {c.kind} cap [{1 / cap:.3g}, {cap:g}]")
            odds *= c.weight
        expected = _prob(odds)
        if chain_ok and abs(expected - e["posterior"]) > POSTERIOR_TOLERANCE:
            report.add("posterior_mismatch",
                       f"{e['_id']}: prior {e['prior']} x weights {[c.weight for c in mine]} gives {expected:.3f}, "
                       f"BELIEFS.md says {e['posterior']}")


def check_effort(run_dir: str, beliefs: list[dict], cells: list[Cell], report: GateReport) -> None:
    """No lazy drops, and every lead a search cell names is a real hypothesis."""
    by_id = {e["_id"] for e in beliefs}
    decisions = _read(run_dir, "DECISIONS.md") or ""
    for e in beliefs:
        if e["state"] != "DROPPED":
            continue
        hid = e["_id"]
        searches = [c for c in cells if c.hypothesis == hid and c.kind == "search"]
        if len(searches) < MIN_SEARCH_BEFORE_DROP:
            report.add("drop_too_early",
                       f"{hid}: DROPPED after {len(searches)} search cell(s); at least {MIN_SEARCH_BEFORE_DROP} are required")
        if not any(_given(c.controls) for c in searches):
            report.add("drop_no_rival_controlled", f"{hid}: DROPPED without a search cell that controls a rival (`controls:`)")
        if not any(_given(c.conditional) for c in searches):
            report.add("drop_no_conditional",
                       f"{hid}: DROPPED without a search cell that tries a regime or conditional split (`conditional:`)")
        if e["posterior"] >= e["prior"]:
            report.add("drop_posterior_not_down",
                       f"{hid}: DROPPED but its posterior {e['posterior']} is not below its prior {e['prior']}")
        if not re.search(rf"(?m)^\s*-?\s*drop {hid}:\s*\S", decisions):
            report.add("drop_no_reason", f"{hid}: DROPPED with no `drop {hid}: <reason>` line in DECISIONS.md")
    for c in cells:
        for ref in re.findall(r"H\d+", c.suggests or ""):
            if ref not in by_id:
                report.add("suggests_unknown_hypothesis",
                           f"cell_{c.nn:02d}: suggests {ref}, which is not an entry in BELIEFS.md")


def k_counts(cells: list[Cell]) -> tuple[int, int]:
    """K_train = every spec evaluated on TRAIN (search variants + confirm runs); K_val = every VAL check."""
    k_train = sum(c.variants for c in cells if c.kind == "search") + sum(1 for c in cells if c.kind == "confirm")
    k_val = sum(1 for c in cells if c.kind == "val")
    return k_train, k_val


def check_stop_reason(run_dir: str, beliefs: list[dict], cands: dict, status: dict, cells: list[Cell],
                      report: GateReport) -> str | None:
    text = _read(run_dir, "STOP_REASON.md")
    if text is None:
        return None
    fields = _parse_kv_file(text, STOP_REQUIRED_KEYS)
    missing = [k for k in STOP_REQUIRED_KEYS if k not in fields or not fields[k]]
    if missing:
        report.add("stop_reason_missing_fields", f"STOP_REASON.md missing field(s) {missing}")
        return None
    rule = fields["rule"]
    if rule not in STOP_RULES:
        report.add("stop_reason_bad_rule", f"STOP_REASON.md rule='{rule}' not one of {STOP_RULES}")
        return None
    if not beliefs:
        return rule

    actual = {
        "open_count": sum(1 for e in beliefs if e["state"] == "OPEN"),
        "dropped_count": sum(1 for e in beliefs if e["state"] == "DROPPED"),
        "frozen_count": len(cands),
        "val_pass_count": sum(1 for s in status.values() if s == "VAL-PASS"),
    }
    for key, n in actual.items():
        try:
            claimed = int(fields[key])
        except ValueError:
            report.add("stop_reason_bad_number", f"STOP_REASON.md {key}='{fields[key]}' not an int")
            continue
        if claimed != n:
            report.add("stop_reason_count_mismatch", f"STOP_REASON.md claims {key}={claimed}, the run actually has {n}")

    try:
        minutes = float(fields["minutes"])
    except ValueError:
        report.add("stop_reason_bad_number", f"STOP_REASON.md minutes='{fields['minutes']}' is not a number")
        minutes = 0.0
    if rule == "S1" and actual["open_count"]:
        report.add("stop_reason_s1_violated", f"STOP_REASON.md claims S1 (no OPEN hypothesis) but {actual['open_count']} are OPEN")
    if rule == "S1" and len(cells) < S1_MIN_CELLS and minutes < S1_MIN_MINUTES:
        report.add("stop_reason_s1_too_early",
                   f"STOP_REASON.md claims S1 after {len(cells)} cells and {minutes:g} minutes; S1 needs at least "
                   f"{S1_MIN_CELLS} cells or {S1_MIN_MINUTES} minutes - spawn new hypotheses instead of stopping")
    if rule == "S3" and len(cells) < S3_CELLS and minutes < S3_MINUTES:
        report.add("stop_reason_s3_under_cap",
                   f"STOP_REASON.md claims S3 (cap) after {len(cells)} cells and {minutes:g} minutes; the cap is "
                   f"{S3_CELLS} cells or {S3_MINUTES} minutes")
    if rule in ("S2", "S3") and not actual["open_count"]:
        report.add("stop_reason_suspicious", f"STOP_REASON.md claims {rule} but no hypothesis is OPEN - that is S1")
    if rule == "S2":
        tail = cells[-DRY_STREAK:]
        if len(tail) < DRY_STREAK or any(c.kind != "search" for c in tail):
            report.add("stop_reason_s2_violated",
                       f"STOP_REASON.md claims S2 but the last {DRY_STREAK} cells are not all search cells")
        elif any(cd.mtime >= tail[0].rule_mtime for cd in cands.values()):
            report.add("stop_reason_s2_violated",
                       f"STOP_REASON.md claims S2 but a candidate was frozen during the last {DRY_STREAK} search cells")
    return rule


# ------------------------------------------------------------------ mode, installs, methods, memory

MODES_ALL = ("A", "B", "C", "D", "E")
SOURCE_METHOD_MODES = ("B", "C")   # a paper is the source: its method must be specified and matched
METHOD_KEYS = ["source", "estimator", "library", "parameters", "sample", "match", "deviation_reason"]
INSTALL_SOURCES = {"pypi", "conda-forge"}
# Imports that need no INSTALLS.md row: the base scientific stack, and the engine's own helpers.
BASE_IMPORTS = {
    "numpy", "pandas", "scipy", "statsmodels", "matplotlib", "seaborn", "pyarrow", "plotly",
    "eda_guard", "cellplot", "data_hygiene",
}
MEMORY_BUDGET_LINES = {"LEDGER.md": 250, "FINDINGS.md": 300, "DATA_FACTS.md": 150}
FINDINGS_MAX_LINES_PER_ENTRY = 3
LEDGER_COLS = ["date", "run", "target", "mode", "stop", "cells", "K_train", "K_val", "dataset",
               "K_cum_train", "K_cum_val", "methods_score"]


def check_mode(run_dir: str, report: GateReport) -> str | None:
    """DECISIONS.md must carry one machine-readable `mode: <A-E>` line."""
    text = _read(run_dir, "DECISIONS.md")
    if text is None:
        return None
    mode = _parse_kv_file(text, ["mode"]).get("mode", "").strip().upper()[:1]
    if mode not in MODES_ALL:
        report.add("decisions_no_mode", "DECISIONS.md has no `mode: <A|B|C|D|E>` line")
        return None
    return mode


def _stdlib() -> set:
    return set(getattr(sys, "stdlib_module_names", ())) | {"__future__"}


def _script_imports(run_dir: str) -> dict:
    """{top-level module name: first file that imports it} over every .py file in the run folder.
    Modules defined by the run's own .py files are local, not installs."""
    pys = glob.glob(_path(run_dir, "**", "*.py"), recursive=True)
    local = {os.path.splitext(os.path.basename(p))[0] for p in pys}
    found = {}
    for p in pys:
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = re.match(r"^\s*(?:from\s+([A-Za-z_]\w*)[\w.]*\s+import|import\s+([A-Za-z_]\w*))", line)
                if m:
                    name = m.group(1) or m.group(2)
                    if name not in local:
                        found.setdefault(name, os.path.relpath(p, run_dir))
    return found


def _parse_table(text: str) -> list[dict]:
    """Rows of the first markdown table in `text`, as dicts keyed by its header row."""
    lines = [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return []
    head = [c.strip() for c in lines[0].strip("|").split("|")]
    rows = []
    for l in lines[2:]:
        cells = [c.strip() for c in l.strip("|").split("|")]
        if len(cells) == len(head):
            rows.append(dict(zip(head, cells)))
    return rows


def check_installs(run_dir: str, report: GateReport) -> None:
    """Every import outside the stdlib and the base stack needs an INSTALLS.md row: a pinned version, an
    allowed source, the claim it serves, what it adds, and a validation file that exists and PASSED."""
    extra = {n: f for n, f in _script_imports(run_dir).items() if n not in _stdlib() and n not in BASE_IMPORTS}
    text = _read(run_dir, "INSTALLS.md")
    rows = {r.get("import", "").strip(): r for r in _parse_table(text)} if text else {}
    for name, where in sorted(extra.items()):
        r = rows.get(name)
        if r is None:
            report.add("install_unlogged", f"`{name}` is imported ({where}) but INSTALLS.md has no row with import={name}")
            continue
        ver = r.get("version", "").strip()
        if not re.match(r"^\d+(\.\d+)*[a-z0-9.+-]*$", ver):
            report.add("install_unpinned", f"INSTALLS.md `{name}`: version '{ver}' is not a pinned version number")
        if r.get("source", "").strip().lower() not in INSTALL_SOURCES:
            report.add("install_bad_source",
                       f"INSTALLS.md `{name}`: source '{r.get('source', '')}' is not one of {sorted(INSTALL_SOURCES)}")
        for col in ("claim", "adds"):
            if r.get(col, "").strip().lower() in ("", "-", "none"):
                report.add("install_no_reason",
                           f"INSTALLS.md `{name}`: '{col}' is empty - name the claim it serves and what it adds over the base stack")
        val = r.get("validation", "").strip()
        if not val or not os.path.exists(_path(run_dir, val)):
            report.add("install_no_validation", f"INSTALLS.md `{name}`: validation file '{val}' does not exist in the run folder")
        if r.get("result", "").strip().upper() != "PASS":
            report.add("install_validation_failed",
                       f"INSTALLS.md `{name}`: validation result is '{r.get('result', '')}', not PASS - an unvalidated tool may not be used")


def check_method_spec(run_dir: str, mode: str | None, beliefs: list[dict], cells: list[Cell],
                      report: GateReport) -> None:
    """Modes B/C: METHOD_SPEC.md specifies the source's method(s) as `## M<n>` blocks, every deviation has a
    reason, and every SOURCE-born hypothesis has a cell citing a defined method (`method: M<n>`)."""
    cited = {c.method for c in cells if c.method}
    text = _read(run_dir, "METHOD_SPEC.md")
    if mode not in SOURCE_METHOD_MODES and text is None:
        if cited:
            report.add("method_unknown_ref", f"cells cite {sorted(cited)} but there is no METHOD_SPEC.md")
        return
    if text is None:
        report.add("method_spec_missing",
                   f"mode {mode}: METHOD_SPEC.md is required (the source's method, specified before any data is opened)")
        return
    blocks = re.split(r"(?m)^##\s*(M\d+)\b", text)
    specs = {blocks[i]: _parse_kv_file(blocks[i + 1], METHOD_KEYS) for i in range(1, len(blocks), 2)}
    if not specs:
        report.add("method_spec_missing", "METHOD_SPEC.md has no `## M<n>` method blocks")
        return
    for mid, kv in specs.items():
        missing = [k for k in METHOD_KEYS if not kv.get(k)]
        if missing:
            report.add("method_spec_bad_entry", f"METHOD_SPEC.md {mid}: missing field(s) {missing}")
            continue
        match = kv["match"].lower()
        if match not in ("exact", "deviation"):
            report.add("method_spec_bad_entry", f"METHOD_SPEC.md {mid}: match='{kv['match']}' is not exact|deviation")
        if match == "deviation" and kv["deviation_reason"].lower() in ("none", "-"):
            report.add("method_deviation_unexplained", f"METHOD_SPEC.md {mid}: deviates from the source with no stated reason")
    for c in cells:
        if c.method and c.method not in specs:
            report.add("method_unknown_ref", f"cell_{c.nn:02d}: method '{c.method}' is not defined in METHOD_SPEC.md")
    if mode in SOURCE_METHOD_MODES:
        for e in beliefs:
            if _born_slice(e) != "SOURCE":
                continue
            if not any(c.hypothesis == e["_id"] and c.method in specs for c in cells):
                report.add("method_not_used",
                           f"{e['_id']} is SOURCE-born in mode {mode} but no cell cites a METHOD_SPEC.md method (`method: M<n>`)")


def memory_dir_for(run_dir: str) -> str:
    """Default MEMORY dir: <eda-routine>/MEMORY, two levels above runs/<run>."""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(run_dir))), "MEMORY")


def _ledger_int(v: str) -> int | None:
    v = (v or "").strip()
    return int(v) if v.isdigit() else None


def check_memory(run_dir: str, memory_dir: str, mode: str | None, beliefs: list[dict], status: dict,
                 cells: list[Cell], report: GateReport) -> None:
    """The run appended its memory, and memory stays inside its budgets (RUNBOOK_v3.md MEMORY)."""
    run = os.path.basename(os.path.normpath(run_dir))
    texts = {}
    for name, budget in MEMORY_BUDGET_LINES.items():
        p = os.path.join(memory_dir, name)
        if not os.path.exists(p):
            report.add("memory_missing", f"{p} does not exist")
            continue
        with open(p, encoding="utf-8") as fh:
            texts[name] = fh.read()
        n = len(texts[name].splitlines())
        if n > budget:
            report.add("memory_over_budget", f"MEMORY/{name} has {n} lines, budget {budget} - consolidate before closing")

    if "LEDGER.md" in texts:
        rows = _parse_table(texts["LEDGER.md"])
        head_line = next((l for l in texts["LEDGER.md"].splitlines() if l.strip().startswith("|")), "")
        header = {c.strip() for c in head_line.strip().strip("|").split("|")}
        if set(LEDGER_COLS) - header:
            report.add("ledger_bad_columns", f"MEMORY/LEDGER.md needs a table with columns {LEDGER_COLS}")
        else:
            mine = [i for i, r in enumerate(rows) if r.get("run") == run]
            if len(mine) != 1:
                report.add("ledger_row_missing" if not mine else "ledger_row_duplicate",
                           f"MEMORY/LEDGER.md has {len(mine)} row(s) for run '{run}'; exactly 1 is required")
            else:
                r = rows[mine[0]]
                need = dict(zip(("K_train", "K_val"), k_counts(cells)))
                for col in ("K_train", "K_val"):
                    k, kcum = _ledger_int(r.get(col)), _ledger_int(r.get(f"K_cum_{col[2:]}"))
                    if k is None or kcum is None:
                        report.add("ledger_bad_number", f"LEDGER row for '{run}': {col} and K_cum_{col[2:]} must be integers")
                        continue
                    if k < need[col]:
                        report.add("ledger_k_too_small", f"LEDGER {col}={k} is below this run's {need[col]}")
                    prev = 0
                    for row in rows[: mine[0]]:
                        if row.get("dataset") == r.get("dataset") and _ledger_int(row.get(f"K_cum_{col[2:]}")) is not None:
                            prev = _ledger_int(row[f"K_cum_{col[2:]}"])
                    if kcum != prev + k:
                        report.add("ledger_bad_kcum",
                                   f"LEDGER K_cum_{col[2:]}={kcum} for dataset '{r.get('dataset')}' should be "
                                   f"{prev} (previous) + {k} = {prev + k}")
                if mode and r.get("mode", "").strip().upper()[:1] != mode:
                    report.add("ledger_mode_mismatch", f"LEDGER mode '{r.get('mode')}' differs from DECISIONS.md mode '{mode}'")
                if r.get("methods_score", "").strip().lower() not in ("pending", "0", "1", "2", "3"):
                    report.add("ledger_bad_score", f"LEDGER methods_score '{r.get('methods_score')}' must be pending or 0-3")

    if "FINDINGS.md" in texts:
        ft = texts["FINDINGS.md"]
        entries = {}
        heads = list(re.finditer(r"(?m)^###\s+(\S+)\s+([HF]\d+)\b.*$", ft))
        for i, m in enumerate(heads):
            end = heads[i + 1].start() if i + 1 < len(heads) else len(ft)
            body = re.split(r"(?m)^#", ft[m.end():end])[0]   # stop at the next heading of any level
            entries[(m.group(1), m.group(2))] = [l for l in body.splitlines() if l.strip()]
        for fid, st in status.items():
            if st not in ("CONFIRM-SHOWN", "VAL-PASS", "VAL-FAIL"):
                continue
            body = entries.get((run, fid))
            if body is None:
                report.add("findings_missing", f"MEMORY/FINDINGS.md has no `### {run} {fid}` entry ({st})")
            elif len(body) > FINDINGS_MAX_LINES_PER_ENTRY:
                report.add("findings_too_long",
                           f"MEMORY/FINDINGS.md `{run} {fid}` has {len(body)} lines, max {FINDINGS_MAX_LINES_PER_ENTRY}")
        for label, ids in (("DROPPED", {e["_id"] for e in beliefs if e["state"] == "DROPPED"}),
                           ("CONFIRM-FAIL", {f for f, st in status.items() if st == "CONFIRM-FAIL"})):
            if not ids:
                continue
            m = re.search(rf"(?m)^-?\s*{re.escape(run)}\s+{label}:\s*(.*)$", ft)
            named = set(re.findall(r"[HF]\d+", m.group(1))) if m else set()
            if ids - named:
                report.add("findings_line_missing", f"MEMORY/FINDINGS.md needs a `{run} {label}: ...` line naming {sorted(ids - named)}")


# ------------------------------------------------------------------ entry point

def check_run(run_dir: str, memory_dir: str | None = None) -> GateReport:
    report = GateReport(run_dir=run_dir)
    if not os.path.isdir(run_dir):
        report.add("no_such_dir", f"{run_dir} is not a directory")
        return report
    check_required_files(run_dir, report)
    check_data_profile_sections(run_dir, report)
    folds = check_splits(run_dir, report)
    beliefs = check_beliefs_format(run_dir, folds, report)
    cands = check_candidates(run_dir, beliefs, report)
    cells = check_cells(run_dir, folds, report)
    status = check_flow(run_dir, beliefs, cands, cells, folds, report)
    check_posteriors(beliefs, cells, report)
    check_effort(run_dir, beliefs, cells, report)
    check_stop_reason(run_dir, beliefs, cands, status, cells, report)
    mode = check_mode(run_dir, report)
    check_installs(run_dir, report)
    check_method_spec(run_dir, mode, beliefs, cells, report)
    check_memory(run_dir, memory_dir or memory_dir_for(run_dir), mode, beliefs, status, cells, report)
    return report


def main(argv: list) -> int:
    args = list(argv[1:])
    memory_dir = None
    if "--memory" in args:
        i = args.index("--memory")
        memory_dir = args[i + 1] if i + 1 < len(args) else None
        del args[i:i + 2]
    if len(args) != 1 or (memory_dir is None and "--memory" in argv):
        print("usage: python gate.py <run_dir> [--memory <MEMORY dir>]")
        return 2
    report = check_run(args[0], memory_dir)
    if report.ok:
        print(f"PASS: {args[0]}")
        return 0
    print(f"FAIL: {args[0]}")
    for i, issue in enumerate(report.issues, 1):
        print(f"  {i}. [{issue.code}] {issue.message}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
