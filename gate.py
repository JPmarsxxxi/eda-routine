"""gate.py - the deterministic check that must PASS before a v3 run writes STATUS: DONE.

Why this exists
----------------
RUNBOOK_v3.md (C:\\Users\\User\\eda-routine\\RUNBOOK_v3.md) describes a process: pre-committed rule
files, a Bayesian ledger with sourced priors, an EXPLORE slice plus several CONFIRM folds with per-
hypothesis slice rules, four stop rules. Prose is advisory - an unattended run under time pressure
can write a plausible REPORT.md without any of that actually having happened, and nothing downstream
would know. This module makes the structural half of the process CHECKED rather than trusted: it
reads the run folder's own files and refuses to pass if what they claim is internally inconsistent.

Same relationship to RUNBOOK_v3.md that eda_guard.py has to data loading: it does not know whether a
hypothesis is a good idea, or whether a decision rule was picked in good faith. It knows whether the
required files exist, whether a rule file predates its result, whether every BELIEFS.md entry carries
every required field, whether each cell's slice is one its hypothesis was allowed to open, whether
each posterior is the product of the weights its result files report, whether each state matches
its posterior and fold record, and whether STOP_REASON.md's claim matches all of that.

What it CANNOT enforce - stated plainly
----------------------------------------
- That a prior's anchor is honestly argued, or that an evidence weight's power simulation was real
  and not invented after the fact.
- That "the largest expected belief shift" was actually the largest available, or that a spawned
  hypothesis's `born_on` / `seen_on` is where it was truly first noticed.
- That a cell's header (hypothesis / slice / kind) describes what its code actually loaded.
- Anything about statistical correctness inside a cell's code.
These need the post-run judge agent (read-only, reads with judgement) that RUNBOOK_v3.md's ENFORCEMENT
section names as gate.py's companion. gate.py is the floor, not the ceiling.

Usage
-----
    python gate.py <run_dir> [--memory <MEMORY dir>]     (default MEMORY dir: <eda-routine>/MEMORY)

Exits 0 and prints PASS if every check passes. Exits 1 and prints FAIL plus every issue, numbered, if
not. `STATUS: DONE` may only be written to TARGET.md after this prints PASS for that run's folder.
"""
from __future__ import annotations

import glob
import os
import re
import sys
from dataclasses import dataclass, field


REQUIRED_STATES = {"OPEN", "LOW", "HIGH", "HIGH-CONFIRM", "HIGH-VAL"}
RESOLVED_STATES = {"LOW", "HIGH-VAL"}  # what S1 requires everything to be
BELIEF_REQUIRED_KEYS = [
    "parent", "source", "question", "hypothesis", "forbids", "rivals",
    "born_on", "seen_on", "prior", "anchor", "posterior", "state",
]
STOP_REQUIRED_KEYS = ["rule", "open_count", "low_count", "high_count", "detail"]
STOP_RULES = ("S1", "S2", "S3", "S4")
CELL_KINDS = {"test", "redirect", "val"}
BRANCHES = {"supported", "refuted", "inconclusive"}

LOW_BELOW = 0.05
HIGH_ABOVE = 0.85
WEIGHT_CAP = 10.0
MIN_CONFIRM_FOLDS = 2
MIN_SUPPORTED_FOLDS = 2   # for HIGH-CONFIRM
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
    branch: str | None = None
    weight: float | None = None
    method: str | None = None   # v3.2: optional `method: M<n>` header (METHOD_SPEC.md id)


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
        m = re.match(r"^([a-z_]+):\s*(.*)$", line.strip())
        if m and m.group(1) in keys and m.group(1) not in out:
            out[m.group(1)] = m.group(2).strip()
    return out


def _odds(p: float) -> float:
    return p / (1.0 - p)


def _prob(odds: float) -> float:
    return odds / (1.0 + odds)


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
    """Split BELIEFS.md on '## H<n>' headings; return one dict per block with
    lowercase keys mapped to their value string (first line only for 'evidence',
    since that key introduces a sub-list rather than a scalar)."""
    blocks = re.split(r"(?m)^##\s*(H\d+)\b", text)
    # re.split with a capturing group interleaves: [preamble, id, body, id, body, ...]
    out = []
    for i in range(1, len(blocks), 2):
        hid, body = blocks[i], blocks[i + 1]
        entry = {"_id": hid, "_raw": body}
        for line in body.splitlines():
            m = re.match(r"^([a-z_]+):\s*(.*)$", line.strip())
            if m:
                key, val = m.group(1), m.group(2).strip()
                if key not in entry:  # first occurrence only (evidence: has no scalar value)
                    entry[key] = val
        out.append(entry)
    return out


def _born_slice(entry: dict) -> str:
    return entry.get("born_on", "").split()[0] if entry.get("born_on") else ""


def _seen_slices(entry: dict) -> set:
    raw = entry.get("seen_on", "none")
    if raw.lower() == "none":
        return set()
    return {s.strip() for s in raw.split(",") if s.strip()}


def _is_no_story(entry: dict) -> bool:
    return entry.get("no_story", "").lower() == "yes" or entry.get("forbids", "").lower().startswith("none")


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
            report.add(
                "beliefs_missing_fields",
                f"{e['_id']}: missing or empty field(s) {missing}",
            )
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
                report.add(
                    "beliefs_bad_number",
                    f"{e['_id']}: {numeric_key}='{e[numeric_key]}' is not a probability strictly between 0 and 1",
                )
        if e["state"] not in REQUIRED_STATES:
            ok = False
            report.add(
                "beliefs_bad_state",
                f"{e['_id']}: state='{e['state']}' is not one of {sorted(REQUIRED_STATES)}",
            )
        if e["parent"].lower() != "none" and not re.match(r"^H\d+$", e["parent"]):
            report.add(
                "beliefs_bad_parent",
                f"{e['_id']}: parent='{e['parent']}' is neither 'none' nor an H<n> id",
            )
        if folds and _born_slice(e) not in valid_born:
            report.add(
                "beliefs_bad_born_on",
                f"{e['_id']}: born_on='{e['born_on']}' must start with SOURCE, EXPLORE or a declared fold {folds}",
            )
        bad_seen = _seen_slices(e) - ({"EXPLORE"} | set(folds))
        if folds and bad_seen:
            report.add(
                "beliefs_bad_seen_on",
                f"{e['_id']}: seen_on names {sorted(bad_seen)}, which are not EXPLORE or a declared fold",
            )
        if ok:
            valid.append(e)
    ids = {e["_id"] for e in entries}
    for e in entries:
        if e.get("parent", "none").lower() != "none" and e["parent"] not in ids:
            report.add(
                "beliefs_dangling_parent",
                f"{e['_id']}: parent '{e['parent']}' does not match any entry in this file",
            )
    return valid


def check_cells(run_dir: str, report: GateReport) -> list[Cell]:
    """Rule-before-result ordering, plus the hypothesis/slice/kind header of every rule file and the
    branch/weight_applied header of every result file. Returns the parsed cells, sorted by number."""
    rule_files = sorted(glob.glob(_path(run_dir, "cells", "cell_*_rule.md")))
    if not rule_files:
        report.add("no_cells", "no cells/cell_*_rule.md found - PHASE 2 produced no test cells")
        return []
    cells = []
    for rule_path in rule_files:
        m = re.search(r"cell_(\d+)_rule\.md$", rule_path)
        if not m:
            continue
        nn = m.group(1)
        result_path = _path(run_dir, "cells", f"cell_{nn}_result.md")
        announce_path = _path(run_dir, "cells", f"cell_{nn}_announce.md")
        if not os.path.exists(announce_path):
            report.add("cell_missing_announce", f"cell_{nn}: no cell_{nn}_announce.md")

        with open(rule_path, encoding="utf-8") as fh:
            head = _parse_kv_file(fh.read(), ["hypothesis", "slice", "kind", "method"])
        missing = [k for k in ("hypothesis", "slice", "kind") if not head.get(k)]
        if missing:
            report.add(
                "cell_rule_no_header",
                f"cell_{nn}: rule.md lacks header line(s) {missing} (hypothesis: H<n> / slice: <name> / kind: <test|redirect|val>)",
            )
            continue
        if head["kind"] not in CELL_KINDS:
            report.add("cell_bad_kind", f"cell_{nn}: kind='{head['kind']}' is not one of {sorted(CELL_KINDS)}")
            continue
        cell = Cell(int(nn), head["hypothesis"], head["slice"], head["kind"], method=head.get("method") or None)

        if not os.path.exists(result_path):
            report.add("cell_missing_result", f"cell_{nn}: no cell_{nn}_result.md")
            cells.append(cell)
            continue
        if os.path.getmtime(result_path) < os.path.getmtime(rule_path):
            report.add(
                "cell_result_before_rule",
                f"cell_{nn}: result.md is older than rule.md - the rule was not written first, "
                f"or the rule file was edited after the result existed",
            )
        with open(result_path, encoding="utf-8") as fh:
            res = _parse_kv_file(fh.read(), ["branch", "weight_applied"])
        if res.get("branch") not in BRANCHES:
            report.add(
                "cell_result_no_branch",
                f"cell_{nn}: result.md has no valid 'branch:' line (one of {sorted(BRANCHES)})",
            )
        else:
            cell.branch = res["branch"]
        try:
            cell.weight = float(res.get("weight_applied", ""))
        except ValueError:
            report.add("cell_result_no_weight", f"cell_{nn}: result.md has no numeric 'weight_applied:' line")
        cells.append(cell)
    return sorted(cells, key=lambda c: c.nn)


def _hypothesis_record(hid: str, cells: list[Cell]) -> dict:
    """Which slices a hypothesis's test cells opened, and its fold / VAL outcomes."""
    tests = [c for c in cells if c.hypothesis == hid and c.kind == "test"]
    vals = [c for c in cells if c.hypothesis == hid and c.kind == "val"]
    fold_tests = [c for c in tests if c.slice.startswith("C")]
    return {
        "opened": [c.slice for c in tests],
        "supported_folds": sum(1 for c in fold_tests if c.branch == "supported"),
        "refuted_folds": sum(1 for c in fold_tests if c.branch == "refuted"),
        "val_supported": any(c.branch == "supported" for c in vals),
        "has_val": bool(vals),
    }


def _admissible(entry: dict, opened: list[str], folds: list[str]) -> list[str]:
    closed = {_born_slice(entry)} | _seen_slices(entry) | set(opened)
    return [s for s in ["EXPLORE"] + folds if s not in closed]


def check_slice_rules(beliefs: list[dict], cells: list[Cell], folds: list[str], report: GateReport) -> None:
    """RUNBOOK_v3.md HOLDOUTS slice rules 1-3, the redirect rule, the NO-STORY block and the VAL rules."""
    by_id = {e["_id"]: e for e in beliefs}
    last_non_val = max((c.nn for c in cells if c.kind != "val"), default=-1)
    opened: dict[str, list[str]] = {hid: [] for hid in by_id}
    fold_branches: dict[str, list[str]] = {hid: [] for hid in by_id}
    val_seen: set = set()

    for c in cells:
        tag = f"cell_{c.nn:02d} ({c.hypothesis}, {c.slice}, {c.kind})"
        e = by_id.get(c.hypothesis)
        if e is None:
            report.add("cell_unknown_hypothesis", f"{tag}: {c.hypothesis} is not an entry in BELIEFS.md")
            continue
        if c.slice not in {"EXPLORE", "VAL"} | set(folds):
            report.add("cell_unknown_slice", f"{tag}: slice is not declared in SPLITS.md")
            continue
        closed = {_born_slice(e)} | _seen_slices(e)

        if c.kind == "test":
            if c.slice == "VAL":
                report.add("cell_val_as_test", f"{tag}: VAL may only be opened by a kind: val cell")
                continue
            if c.slice in closed:
                report.add(
                    "slice_birth_or_seen",
                    f"{tag}: {c.hypothesis} was born on or has already seen {c.slice} (born_on / seen_on)",
                )
            if c.slice in opened[c.hypothesis]:
                report.add("slice_opened_twice", f"{tag}: {c.hypothesis} already opened {c.slice}")
            if c.slice.startswith("C"):
                expected = next((f for f in folds if f not in closed and f not in opened[c.hypothesis]), None)
                if expected is not None and c.slice != expected:
                    report.add(
                        "slice_fold_skipped",
                        f"{tag}: {c.hypothesis}'s next admissible fold was {expected} (folds open in order)",
                    )
                if _is_no_story(e) and e["forbids"].lower().startswith("none"):
                    report.add(
                        "slice_no_story_on_fold",
                        f"{tag}: {c.hypothesis} is NO-STORY with no forbidding prediction; it may not open a CONFIRM fold",
                    )
                if c.branch:
                    fold_branches[c.hypothesis].append(c.branch)
            opened[c.hypothesis].append(c.slice)

        elif c.kind == "redirect":
            if c.slice != "EXPLORE" and c.slice not in opened[c.hypothesis]:
                report.add(
                    "redirect_unopened_slice",
                    f"{tag}: a redirect may look at EXPLORE or a slice {c.hypothesis} already opened, not {c.slice}",
                )
            if c.weight is not None and abs(c.weight - 1.0) > 1e-9:
                report.add("redirect_weight", f"{tag}: a redirect cell's weight_applied must be 1, not {c.weight}")

        elif c.kind == "val":
            if c.slice != "VAL":
                report.add("val_wrong_slice", f"{tag}: a kind: val cell must have slice: VAL")
            if c.nn < last_non_val:
                report.add("val_before_tests", f"{tag}: VAL cells must come after every test and redirect cell")
            if c.hypothesis in val_seen:
                report.add("val_opened_twice", f"{tag}: {c.hypothesis} already had a VAL cell")
            val_seen.add(c.hypothesis)
            sup = fold_branches[c.hypothesis].count("supported")
            ref = fold_branches[c.hypothesis].count("refuted")
            if sup < MIN_SUPPORTED_FOLDS or ref > 0:
                report.add(
                    "val_not_high_confirm",
                    f"{tag}: VAL is only for HIGH-CONFIRM; {c.hypothesis} had {sup} supported and {ref} refuted folds",
                )


def check_posteriors_and_states(beliefs: list[dict], cells: list[Cell], report: GateReport) -> None:
    for e in beliefs:
        hid = e["_id"]
        mine = [c for c in cells if c.hypothesis == hid]
        odds = _odds(e["prior"])
        chain_ok = True
        for c in mine:
            if c.weight is None:
                chain_ok = False
                continue
            if not (1.0 / WEIGHT_CAP - 1e-9 <= c.weight <= WEIGHT_CAP + 1e-9):
                report.add(
                    "weight_over_cap",
                    f"cell_{c.nn:02d}: weight_applied {c.weight} is outside the 10x cap [0.1, 10] (guard b)",
                )
            odds *= c.weight
        expected = _prob(odds)
        if chain_ok and abs(expected - e["posterior"]) > POSTERIOR_TOLERANCE:
            report.add(
                "posterior_mismatch",
                f"{hid}: prior {e['prior']} x weights {[c.weight for c in mine]} gives {expected:.3f}, "
                f"BELIEFS.md says {e['posterior']}",
            )

        rec = _hypothesis_record(hid, cells)
        post, state = e["posterior"], e["state"]
        if post < LOW_BELOW:
            band = "LOW"
        elif post <= HIGH_ABOVE:
            band = "OPEN"
        else:
            band = "HIGH"
        if band != "HIGH" and state != band:
            report.add("state_mismatch", f"{hid}: posterior {post} means state {band}, BELIEFS.md says {state}")
            continue
        if band == "HIGH":
            if not state.startswith("HIGH"):
                report.add("state_mismatch", f"{hid}: posterior {post} means a HIGH state, BELIEFS.md says {state}")
                continue
            confirmed = rec["supported_folds"] >= MIN_SUPPORTED_FOLDS and rec["refuted_folds"] == 0
            if state == "HIGH-VAL" and not (confirmed and rec["val_supported"]):
                report.add("state_mismatch", f"{hid}: HIGH-VAL needs HIGH-CONFIRM and a supported VAL cell")
            elif state == "HIGH-CONFIRM" and not confirmed:
                report.add(
                    "state_mismatch",
                    f"{hid}: HIGH-CONFIRM needs >= {MIN_SUPPORTED_FOLDS} supported and 0 refuted folds; "
                    f"has {rec['supported_folds']} supported, {rec['refuted_folds']} refuted",
                )
            elif state == "HIGH-CONFIRM" and rec["val_supported"]:
                report.add("state_mismatch", f"{hid}: passed VAL, so its state is HIGH-VAL, not HIGH-CONFIRM")
            elif state == "HIGH" and confirmed:
                report.add("state_mismatch", f"{hid}: meets HIGH-CONFIRM (folds) but is recorded as HIGH")
        if state == "HIGH-CONFIRM" and not rec["has_val"]:
            report.add("val_owed", f"{hid}: HIGH-CONFIRM at the end of the session but no VAL cell was run")


def check_stop_reason(run_dir: str, beliefs: list[dict], cells: list[Cell], folds: list[str],
                      report: GateReport) -> None:
    text = _read(run_dir, "STOP_REASON.md")
    if text is None:
        return
    fields = _parse_kv_file(text, STOP_REQUIRED_KEYS)
    missing = [k for k in STOP_REQUIRED_KEYS if k not in fields or not fields[k]]
    if missing:
        report.add("stop_reason_missing_fields", f"STOP_REASON.md missing field(s) {missing}")
        return
    rule = fields["rule"]
    if rule not in STOP_RULES:
        report.add("stop_reason_bad_rule", f"STOP_REASON.md rule='{rule}' not one of {STOP_RULES}")
        return

    if not beliefs:
        return  # already reported

    actual_open = sum(1 for e in beliefs if e.get("state") == "OPEN")
    actual_low = sum(1 for e in beliefs if e.get("state") == "LOW")
    actual_high = sum(1 for e in beliefs if e.get("state", "").startswith("HIGH"))

    for key, actual in (("open_count", actual_open), ("low_count", actual_low),
                        ("high_count", actual_high)):
        try:
            claimed = int(fields[key])
        except ValueError:
            report.add("stop_reason_bad_number", f"STOP_REASON.md {key}='{fields[key]}' not an int")
            continue
        if claimed != actual:
            report.add(
                "stop_reason_count_mismatch",
                f"STOP_REASON.md claims {key}={claimed}, BELIEFS.md actually has {actual}",
            )

    unresolved = [e["_id"] for e in beliefs if e["state"] not in RESOLVED_STATES]
    pickable = [
        e["_id"] for e in beliefs
        if e["state"] in ("OPEN", "HIGH")
        and _admissible(e, _hypothesis_record(e["_id"], cells)["opened"], folds)
    ]
    if rule == "S1" and unresolved:
        report.add(
            "stop_reason_s1_violated",
            f"STOP_REASON.md claims S1 (all LOW or HIGH-VAL) but {unresolved} are not",
        )
    if rule == "S4" and pickable:
        report.add(
            "stop_reason_s4_violated",
            f"STOP_REASON.md claims S4 (slices exhausted) but {pickable} still have an admissible slice",
        )
    if rule == "S2" and not pickable:
        report.add(
            "stop_reason_s2_no_tests",
            "STOP_REASON.md claims S2 but no hypothesis has an admissible slice left - that is S4 (or S1)",
        )
    if rule in ("S2", "S3", "S4") and not unresolved:
        report.add(
            "stop_reason_suspicious",
            f"STOP_REASON.md claims {rule} but every hypothesis is LOW or HIGH-VAL - this should have been S1",
        )


# ------------------------------------------------------------------ v3.2: mode, installs, methods, memory

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
FINDINGS_MIN_MOVE = 0.05   # a hypothesis that moved this far off its prior (and is not LOW) gets a FINDINGS entry
LEDGER_COLS = ["date", "run", "target", "mode", "stop", "cells", "K", "dataset", "K_cum", "methods_score"]


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
    reason, and every SOURCE-born hypothesis has a test cell citing a defined method (`method: M<n>`)."""
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
            if not any(c.hypothesis == e["_id"] and c.kind in ("test", "val") and c.method in specs for c in cells):
                report.add("method_not_used",
                           f"{e['_id']} is SOURCE-born in mode {mode} but no test cell cites a METHOD_SPEC.md method (`method: M<n>`)")


def memory_dir_for(run_dir: str) -> str:
    """Default MEMORY dir: <eda-routine>/MEMORY, two levels above runs/<run>."""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(run_dir))), "MEMORY")


def check_memory(run_dir: str, memory_dir: str, mode: str | None, beliefs: list[dict], cells: list[Cell],
                 report: GateReport) -> None:
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
                scored = sum(1 for c in cells if c.kind in ("test", "val"))
                try:
                    k, kcum = int(r["K"]), int(r["K_cum"])
                    if k < scored:
                        report.add("ledger_k_too_small", f"LEDGER K={k} is below this run's {scored} scored slice openings")
                    prev = 0
                    for row in rows[: mine[0]]:
                        if row.get("dataset") == r.get("dataset") and row.get("K_cum", "").isdigit():
                            prev = int(row["K_cum"])
                    if kcum != prev + k:
                        report.add("ledger_bad_kcum",
                                   f"LEDGER K_cum={kcum} for dataset '{r.get('dataset')}' should be {prev} (previous) + {k} = {prev + k}")
                except ValueError:
                    report.add("ledger_bad_number", f"LEDGER row for '{run}': K and K_cum must be integers")
                if mode and r.get("mode", "").strip().upper()[:1] != mode:
                    report.add("ledger_mode_mismatch", f"LEDGER mode '{r.get('mode')}' differs from DECISIONS.md mode '{mode}'")
                if r.get("methods_score", "").strip().lower() not in ("pending", "0", "1", "2", "3"):
                    report.add("ledger_bad_score", f"LEDGER methods_score '{r.get('methods_score')}' must be pending or 0-3")

    if "FINDINGS.md" in texts:
        ft = texts["FINDINGS.md"]
        entries = {}
        heads = list(re.finditer(r"(?m)^###\s+(\S+)\s+(H\d+)\b.*$", ft))
        for i, m in enumerate(heads):
            end = heads[i + 1].start() if i + 1 < len(heads) else len(ft)
            body = ft[m.end():end]
            body = re.split(r"(?m)^#", body)[0]   # stop at the next heading of any level
            entries[(m.group(1), m.group(2))] = [l for l in body.splitlines() if l.strip()]
        for e in beliefs:
            moved = abs(float(e["posterior"]) - float(e["prior"])) >= FINDINGS_MIN_MOVE
            if e["state"] == "LOW" or not moved:
                continue
            body = entries.get((run, e["_id"]))
            if body is None:
                report.add("findings_missing",
                           f"MEMORY/FINDINGS.md has no `### {run} {e['_id']}` entry ({e['state']}, {e['prior']} -> {e['posterior']})")
            elif len(body) > FINDINGS_MAX_LINES_PER_ENTRY:
                report.add("findings_too_long",
                           f"MEMORY/FINDINGS.md `{run} {e['_id']}` has {len(body)} lines, max {FINDINGS_MAX_LINES_PER_ENTRY}")
        lows = {e["_id"] for e in beliefs if e["state"] == "LOW"}
        if lows:
            m = re.search(rf"(?m)^-?\s*{re.escape(run)}\s+LOW:\s*(.*)$", ft)
            named = set(re.findall(r"H\d+", m.group(1))) if m else set()
            if lows - named:
                report.add("findings_low_line_missing",
                           f"MEMORY/FINDINGS.md needs a `{run} LOW: ...` line naming {sorted(lows - named)}")

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
    cells = check_cells(run_dir, report)
    check_slice_rules(beliefs, cells, folds, report)
    check_posteriors_and_states(beliefs, cells, report)
    check_stop_reason(run_dir, beliefs, cells, folds, report)
    mode = check_mode(run_dir, report)
    check_installs(run_dir, report)
    check_method_spec(run_dir, mode, beliefs, cells, report)
    check_memory(run_dir, memory_dir or memory_dir_for(run_dir), mode, beliefs, cells, report)
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
    argv = [argv[0], args[0]]
    report = check_run(argv[1], memory_dir)
    if report.ok:
        print(f"PASS: {argv[1]}")
        return 0
    print(f"FAIL: {argv[1]}")
    for i, issue in enumerate(report.issues, 1):
        print(f"  {i}. [{issue.code}] {issue.message}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
