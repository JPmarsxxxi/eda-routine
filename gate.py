"""gate.py - the deterministic check that must PASS before a v3 run writes STATUS: DONE.

Why this exists
----------------
RUNBOOK_v3.md (C:\\Users\\User\\eda-routine\\RUNBOOK_v3.md) describes a process: pre-committed rule
files, a Bayesian ledger with sourced priors, three stop rules, one CONFIRM opening per hypothesis.
Prose is advisory - an unattended run under time pressure can write a plausible REPORT.md without any
of that actually having happened, and nothing downstream would know. This module makes the structural
half of the process CHECKED rather than trusted: it reads the run folder's own files and refuses to
pass if what they claim is internally inconsistent.

Same relationship to RUNBOOK_v3.md that eda_guard.py has to data loading: it does not know whether a
hypothesis is a good idea, or whether a decision rule was picked in good faith. It knows whether the
required files exist, whether a rule file predates the result it supposedly preceded, whether every
BELIEFS.md entry carries every required field in the fixed format RUNBOOK_v3.md section "BELIEFS.md
format" defines, and whether STOP_REASON.md's claim matches what BELIEFS.md actually shows.

What it CANNOT enforce - stated plainly
----------------------------------------
- That a prior's anchor is honestly argued, or that an evidence weight's power simulation was real
  and not invented after the fact.
- That "the largest expected belief shift" was actually the largest available, or that a spawned
  hypothesis's `born_on` slice is the slice it was truly first noticed on.
- That a NO-STORY entry was genuinely re-written with a real `forbids` line before its CONFIRM cell,
  rather than edited to *look* re-written - it only checks the file states as required now.
- Anything about statistical correctness inside a cell's code.
These need the post-run judge agent (read-only, reads with judgement) that RUNBOOK_v3.md's ENFORCEMENT
section names as gate.py's companion. gate.py is the floor, not the ceiling.

Usage
-----
    python gate.py <run_dir>

Exits 0 and prints PASS if every check passes. Exits 1 and prints FAIL plus every issue, numbered, if
not. `STATUS: DONE` may only be written to TARGET.md after this prints PASS for that run's folder.
"""
from __future__ import annotations

import glob
import os
import re
import sys
from dataclasses import dataclass, field


REQUIRED_STATES = {"OPEN", "LOW", "HIGH-EXPLORE", "HIGH-CONFIRM", "HIGH-VAL"}
RESOLVED_STATES = {"LOW", "HIGH-VAL"}  # what S1 requires everything to be
BELIEF_REQUIRED_KEYS = [
    "parent", "source", "question", "hypothesis", "forbids", "rivals",
    "born_on", "prior", "anchor", "posterior", "state",
]
STOP_REQUIRED_KEYS = ["rule", "open_count", "low_count", "high_count", "detail"]

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


# ------------------------------------------------------------------ file helpers

def _path(run_dir: str, *parts: str) -> str:
    return os.path.join(run_dir, *parts)


def _read(run_dir: str, *parts: str):
    p = _path(run_dir, *parts)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as fh:
        return fh.read()


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


def _parse_belief_blocks(text: str) -> list[dict]:
    """Split BELIEFS.md on '## H<n>' headings; return one dict per block with
    lowercase keys mapped to their value string (first line only for 'evidence',
    since that key introduces a sub-list rather than a scalar)."""
    blocks = re.split(r"(?m)^##\s*(H\d+)", text)
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


def check_beliefs_format(run_dir: str, report: GateReport) -> list[dict]:
    text = _read(run_dir, "BELIEFS.md")
    if text is None:
        return []
    entries = _parse_belief_blocks(text)
    if not entries:
        report.add("beliefs_empty", "BELIEFS.md has no '## H<n>' entries")
        return []
    for e in entries:
        missing = [k for k in BELIEF_REQUIRED_KEYS if not e.get(k)]
        if missing:
            report.add(
                "beliefs_missing_fields",
                f"{e['_id']}: missing or empty field(s) {missing}",
            )
            continue
        if e["forbids"].lower().startswith("none") and "no-story" not in e["forbids"].lower():
            report.add(
                "beliefs_no_forbid",
                f"{e['_id']}: 'forbids' is empty of content but not marked NO-STORY "
                f"('forbids: none - NO-STORY' is the only accepted empty form)",
            )
        for numeric_key in ("prior", "posterior"):
            try:
                v = float(e[numeric_key])
                if not (0.0 <= v <= 1.0):
                    raise ValueError
            except ValueError:
                report.add(
                    "beliefs_bad_number",
                    f"{e['_id']}: {numeric_key}='{e[numeric_key]}' is not a probability in [0, 1]",
                )
        if e["state"] not in REQUIRED_STATES:
            report.add(
                "beliefs_bad_state",
                f"{e['_id']}: state='{e['state']}' is not one of {sorted(REQUIRED_STATES)}",
            )
        if e["parent"].lower() != "none" and not re.match(r"^H\d+$", e["parent"]):
            report.add(
                "beliefs_bad_parent",
                f"{e['_id']}: parent='{e['parent']}' is neither 'none' nor an H<n> id",
            )
    ids = {e["_id"] for e in entries}
    for e in entries:
        if e.get("parent", "none").lower() != "none" and e["parent"] not in ids:
            report.add(
                "beliefs_dangling_parent",
                f"{e['_id']}: parent '{e['parent']}' does not match any entry in this file",
            )
    return entries


def check_cell_rule_precedes_result(run_dir: str, report: GateReport) -> None:
    """For every cell_NN_rule.md, its cell_NN_result.md (if present) must not be OLDER than the
    rule file - i.e. the rule was written first. This is an mtime proxy, not a cryptographic
    guarantee (see module docstring); it catches the ordinary case of a rule edited after the
    fact, which updates its mtime forward past the result's."""
    rule_files = sorted(glob.glob(_path(run_dir, "cells", "cell_*_rule.md")))
    if not rule_files:
        report.add("no_cells", "no cells\\cell_*_rule.md found - PHASE 2 produced no test cells")
        return
    for rule_path in rule_files:
        m = re.search(r"cell_(\d+)_rule\.md$", rule_path)
        if not m:
            continue
        nn = m.group(1)
        result_path = _path(run_dir, "cells", f"cell_{nn}_result.md")
        announce_path = _path(run_dir, "cells", f"cell_{nn}_announce.md")
        if not os.path.exists(announce_path):
            report.add("cell_missing_announce", f"cell_{nn}: no cell_{nn}_announce.md")
        if not os.path.exists(result_path):
            report.add("cell_missing_result", f"cell_{nn}: no cell_{nn}_result.md")
            continue
        if os.path.getmtime(result_path) < os.path.getmtime(rule_path):
            report.add(
                "cell_result_before_rule",
                f"cell_{nn}: result.md is older than rule.md - the rule was not written first, "
                f"or the rule file was edited after the result existed",
            )


def _parse_kv_file(text: str, required_keys: list[str]) -> dict:
    out = {}
    for line in text.splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line.strip())
        if m and m.group(1) in required_keys:
            out[m.group(1)] = m.group(2).strip()
    return out


def check_stop_reason(run_dir: str, beliefs: list[dict], report: GateReport) -> None:
    text = _read(run_dir, "STOP_REASON.md")
    if text is None:
        return
    fields = _parse_kv_file(text, STOP_REQUIRED_KEYS)
    missing = [k for k in STOP_REQUIRED_KEYS if k not in fields or not fields[k]]
    if missing:
        report.add("stop_reason_missing_fields", f"STOP_REASON.md missing field(s) {missing}")
        return
    if fields["rule"] not in ("S1", "S2", "S3"):
        report.add("stop_reason_bad_rule", f"STOP_REASON.md rule='{fields['rule']}' not S1/S2/S3")
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

    if fields["rule"] == "S1" and actual_open != 0:
        report.add(
            "stop_reason_s1_violated",
            f"STOP_REASON.md claims S1 (all resolved) but BELIEFS.md has {actual_open} OPEN entries",
        )
    if fields["rule"] in ("S2", "S3") and actual_open == 0:
        report.add(
            "stop_reason_suspicious",
            f"STOP_REASON.md claims {fields['rule']} but every hypothesis is already resolved - "
            f"this should have been S1",
        )


def check_confirm_without_rule(run_dir: str, beliefs: list[dict], report: GateReport) -> None:
    """Best-effort: a HIGH-CONFIRM or HIGH-VAL hypothesis must be named in at least one cell's
    rule file, since every CONFIRM/VAL opening is supposed to be a cell with its rule written
    first (checked structurally by check_cell_rule_precedes_result already). This only checks
    that the id is mentioned somewhere in the cells directory - it cannot confirm the mention
    is the actual opening rule, only that no HIGH hypothesis is completely un-referenced."""
    rule_texts = []
    for p in glob.glob(_path(run_dir, "cells", "cell_*_rule.md")):
        with open(p, encoding="utf-8") as fh:
            rule_texts.append(fh.read())
    joined = "\n".join(rule_texts)
    for e in beliefs:
        if e.get("state", "").startswith("HIGH") and e["_id"] not in joined:
            report.add(
                "high_belief_unreferenced",
                f"{e['_id']} is state={e['state']} but is not named in any cells\\cell_*_rule.md - "
                f"a HIGH hypothesis's CONFIRM/VAL opening must cite its own id in the rule file",
            )


# ------------------------------------------------------------------ entry point

def check_run(run_dir: str) -> GateReport:
    report = GateReport(run_dir=run_dir)
    if not os.path.isdir(run_dir):
        report.add("no_such_dir", f"{run_dir} is not a directory")
        return report
    check_required_files(run_dir, report)
    check_data_profile_sections(run_dir, report)
    beliefs = check_beliefs_format(run_dir, report)
    check_cell_rule_precedes_result(run_dir, report)
    check_stop_reason(run_dir, beliefs, report)
    check_confirm_without_rule(run_dir, beliefs, report)
    return report


def main(argv: list) -> int:
    if len(argv) != 2:
        print("usage: python gate.py <run_dir>")
        return 2
    report = check_run(argv[1])
    if report.ok:
        print(f"PASS: {argv[1]}")
        return 0
    print(f"FAIL: {argv[1]}")
    for i, issue in enumerate(report.issues, 1):
        print(f"  {i}. [{issue.code}] {issue.message}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
