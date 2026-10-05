"""Tests for gate.py. Run: python -m unittest discover -s tests

Each test builds a small, synthetic v3 run folder that passes the gate, breaks one rule, and checks
the gate names that rule. The run is not real data - only the files gate.py reads.
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gate  # noqa: E402


SPLITS = """# SPLITS
slices:
- EXPLORE 2017-08-17 2021-07-01
- C1 2021-07-08 2022-01-01
- C2 2022-01-08 2022-07-01
- C3 2022-07-08 2023-03-20
- VAL 2023-03-25 2023-12-01
"""


def belief(hid, title, born_on, prior, posterior, state, parent="none", seen_on="none",
           forbids="a positive IC on the next fold"):
    return f"""## {hid} — {title}
parent: {parent}
source: OBSERVATIONS.md #1
question: does it?
hypothesis: a change in close predicts the next block because of a reason
forbids: {forbids}
rivals: volatility; time of day
born_on: {born_on}
seen_on: {seen_on}
prior: {prior}
anchor: uninformative default 0.4
posterior: {posterior}
state: {state}
evidence:
- see cells
"""


def base_beliefs():
    # H1: 0.40 -> C1 x10 -> C2 x10 -> VAL x10 = 0.9985, HIGH-VAL.
    # H2: 0.30 -> C1 x0.1 = 0.041, LOW; its redirect spawned H3, still OPEN and untested.
    return {
        "H1": dict(title="6h reversal", born_on="EXPLORE #1", prior=0.40, posterior=0.998, state="HIGH-VAL"),
        "H2": dict(title="daily reversal", born_on="EXPLORE #2", prior=0.30, posterior=0.041, state="LOW"),
        "H3": dict(title="crash rebound", born_on="EXPLORE cell_04", prior=0.30, posterior=0.30, state="OPEN",
                   parent="H2"),
    }


def base_cells():
    # nn: (hypothesis, slice, kind, branch, weight)
    return {
        1: ("H1", "C1", "test", "supported", 10),
        2: ("H1", "C2", "test", "supported", 10),
        3: ("H2", "C1", "test", "refuted", 0.1),
        4: ("H2", "EXPLORE", "redirect", "inconclusive", 1),
        5: ("H1", "VAL", "val", "supported", 10),
    }


BASE_STOP = dict(rule="S2", open_count=1, low_count=1, high_count=1,
                 detail="three picks at <= 3 pp")


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


RUN = "2026-01-01_test"
LEDGER_HEAD = ("| date | run | target | mode | stop | cells | K | dataset | K_cum | methods_score |\n"
               "|---|---|---|---|---|---|---|---|---|---|\n")


def memory_files(beliefs, cells, mode="E", k=None, k_cum=None, score="pending", prior_rows=""):
    """Valid MEMORY/ contents for a run: one LEDGER row, a FINDINGS entry per moved non-LOW hypothesis,
    one LOW line, an empty-ish DATA_FACTS."""
    scored = sum(1 for c in cells.values() if c[2] in ("test", "val"))
    k = scored if k is None else k
    k_cum = k if k_cum is None else k_cum
    ledger = LEDGER_HEAD + prior_rows + (
        f"| 2026-01-01 | {RUN} | test | {mode} | S2 | {len(cells)} | {k} | ds1 | {k_cum} | {score} |\n")
    findings = "# FINDINGS\n\n"
    lows = [h for h, kw in beliefs.items() if kw["state"] == "LOW"]
    if lows:
        findings += f"- {RUN} LOW: {', '.join(lows)}\n\n"
    for h, kw in beliefs.items():
        if kw["state"] != "LOW" and abs(kw["posterior"] - kw["prior"]) >= 0.05:
            findings += f"### {RUN} {h} — {kw['title']}\nclaim and state in one line\nneeds: nothing\n\n"
    return {"LEDGER.md": ledger, "FINDINGS.md": findings, "DATA_FACTS.md": "# DATA_FACTS\n- ds1: fact\n"}


class GateTest(unittest.TestCase):
    def build(self, beliefs=None, cells=None, stop=None, splits=SPLITS, mode="E", memory=None, files=None):
        """Synthetic run at <tmp>/runs/<RUN> with its MEMORY at <tmp>/MEMORY (gate's default location).
        `memory` overrides individual MEMORY files; `files` adds or replaces files in the run folder.
        A cell tuple may carry a 6th element: its `method:` header."""
        beliefs = beliefs if beliefs is not None else base_beliefs()
        cells = cells if cells is not None else base_cells()
        stop = stop if stop is not None else BASE_STOP
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        d = os.path.join(tmp.name, "runs", RUN)
        os.makedirs(d)
        for name in gate.REQUIRED_FILES:
            write(os.path.join(d, name), f"# {name}\n")
        write(os.path.join(d, "DECISIONS.md"), f"# DECISIONS\nmode: {mode}\n")
        mem = memory_files(beliefs, cells, mode)
        mem.update(memory or {})
        for name, text in mem.items():
            if text is not None:
                write(os.path.join(tmp.name, "MEMORY", name), text)
        write(os.path.join(d, "DATA_PROFILE.md"), "".join(f"## {i}. section\n" for i in range(1, 8)))
        write(os.path.join(d, "SPLITS.md"), splits)
        write(os.path.join(d, "BELIEFS.md"), "# BELIEFS\n\n" + "\n".join(belief(h, **kw) for h, kw in beliefs.items()))
        write(os.path.join(d, "STOP_REASON.md"), "".join(f"{k}: {v}\n" for k, v in stop.items()))
        os.makedirs(os.path.join(d, "cells"))
        for nn, (hid, sl, kind, branch, weight, *rest) in cells.items():
            p = os.path.join(d, "cells", f"cell_{nn:02d}_")
            method = f"method: {rest[0]}\n" if rest else ""
            write(p + "rule.md", f"hypothesis: {hid}\nslice: {sl}\nkind: {kind}\n{method}\n# rule\n")
            write(p + "announce.md", "# announce\n")
            write(p + "result.md", f"branch: {branch}\nweight_applied: {weight}\n\n# result\n")
        for name, text in (files or {}).items():
            write(os.path.join(d, name), text)
        return gate.check_run(d)

    def codes(self, report):
        return {i.code for i in report.issues}

    def assertFails(self, report, code):
        self.assertIn(code, self.codes(report), [f"{i.code}: {i.message}" for i in report.issues])

    # ---------------------------------------------------------------- the baseline

    def test_baseline_passes(self):
        report = self.build()
        self.assertTrue(report.ok, [f"{i.code}: {i.message}" for i in report.issues])

    # ---------------------------------------------------------------- splits

    def test_one_fold_is_too_few(self):
        splits = SPLITS.replace("- C2 2022-01-08 2022-07-01\n", "").replace("- C3 2022-07-08 2023-03-20\n", "")
        self.assertFails(self.build(splits=splits), "splits_too_few_folds")

    def test_missing_slices_block(self):
        self.assertFails(self.build(splits="# SPLITS\nEXPLORE then CONFIRM\n"), "splits_no_block")

    def test_overlapping_folds(self):
        splits = SPLITS.replace("- C2 2022-01-08", "- C2 2021-12-01")
        self.assertFails(self.build(splits=splits), "splits_overlap")

    # ---------------------------------------------------------------- slice rules

    def test_test_on_birth_slice(self):
        cells = base_cells()
        cells[6] = ("H3", "EXPLORE", "test", "inconclusive", 1)
        cells[5], cells[6] = cells[6], cells[5]  # keep VAL last
        self.assertFails(self.build(cells=cells), "slice_birth_or_seen")

    def test_test_on_seen_slice(self):
        beliefs = base_beliefs()
        beliefs["H3"]["seen_on"] = "C1"
        cells = base_cells()
        cells[5] = ("H3", "C1", "test", "inconclusive", 1)
        cells[6] = ("H1", "VAL", "val", "supported", 10)
        self.assertFails(self.build(beliefs=beliefs, cells=cells), "slice_birth_or_seen")

    def test_fold_skipped(self):
        cells = base_cells()
        cells[2] = ("H1", "C3", "test", "supported", 10)
        self.assertFails(self.build(cells=cells), "slice_fold_skipped")

    def test_slice_opened_twice(self):
        cells = base_cells()
        cells[2] = ("H1", "C1", "test", "supported", 10)
        self.assertFails(self.build(cells=cells), "slice_opened_twice")

    def test_child_born_on_fold_may_use_explore_and_other_folds(self):
        beliefs = base_beliefs()
        # H3 born on C1; tested on EXPLORE (x2) then C2 (x2): 0.30 -> 0.632. C1 is skipped because it is closed.
        beliefs["H3"].update(born_on="C1 cell_03", posterior=0.632)
        cells = base_cells()
        cells[5] = ("H3", "EXPLORE", "test", "supported", 2)
        cells[6] = ("H3", "C2", "test", "supported", 2)
        cells[7] = ("H1", "VAL", "val", "supported", 10)
        report = self.build(beliefs=beliefs, cells=cells)
        self.assertTrue(report.ok, [f"{i.code}: {i.message}" for i in report.issues])

    def test_redirect_on_unopened_fold(self):
        cells = base_cells()
        cells[4] = ("H2", "C2", "redirect", "inconclusive", 1)
        self.assertFails(self.build(cells=cells), "redirect_unopened_slice")

    def test_no_story_on_fold(self):
        beliefs = base_beliefs()
        beliefs["H2"]["forbids"] = "none - NO-STORY"
        self.assertFails(self.build(beliefs=beliefs), "slice_no_story_on_fold")

    # ---------------------------------------------------------------- VAL

    def test_val_after_one_fold(self):
        cells = base_cells()
        del cells[2]
        beliefs = base_beliefs()
        beliefs["H1"].update(posterior=0.985)
        self.assertFails(self.build(beliefs=beliefs, cells=cells), "val_not_high_confirm")

    def test_val_before_tests(self):
        cells = base_cells()
        cells[3], cells[5] = cells[5], cells[3]
        self.assertFails(self.build(cells=cells), "val_before_tests")

    def test_high_confirm_without_val(self):
        cells = base_cells()
        del cells[5]
        beliefs = base_beliefs()
        beliefs["H1"].update(posterior=0.985, state="HIGH-CONFIRM")
        self.assertFails(self.build(beliefs=beliefs, cells=cells), "val_owed")

    # ---------------------------------------------------------------- posteriors and states

    def test_posterior_mismatch(self):
        beliefs = base_beliefs()
        beliefs["H2"]["posterior"] = 0.15
        beliefs["H2"]["state"] = "OPEN"
        self.assertFails(self.build(beliefs=beliefs), "posterior_mismatch")

    def test_weight_over_cap(self):
        cells = base_cells()
        cells[3] = ("H2", "C1", "test", "refuted", 0.01)
        beliefs = base_beliefs()
        beliefs["H2"]["posterior"] = 0.004
        self.assertFails(self.build(beliefs=beliefs, cells=cells), "weight_over_cap")

    def test_state_does_not_match_posterior(self):
        beliefs = base_beliefs()
        beliefs["H2"]["state"] = "OPEN"
        self.assertFails(self.build(beliefs=beliefs), "state_mismatch")

    def test_high_confirm_needs_two_folds(self):
        cells = base_cells()
        del cells[2]
        del cells[5]
        beliefs = base_beliefs()
        beliefs["H1"].update(posterior=0.870, state="HIGH-CONFIRM")
        self.assertFails(self.build(beliefs=beliefs, cells=cells), "state_mismatch")

    def test_refuted_fold_blocks_high_confirm(self):
        # H1: C1 x10, C2 x0.5, C3 x10 -> 0.97, but a refuted fold means it is HIGH, not HIGH-CONFIRM.
        cells = base_cells()
        cells[2] = ("H1", "C2", "test", "refuted", 0.5)
        cells[5] = ("H1", "C3", "test", "supported", 10)
        beliefs = base_beliefs()
        beliefs["H1"].update(posterior=0.971, state="HIGH-CONFIRM")
        self.assertFails(self.build(beliefs=beliefs, cells=cells), "state_mismatch")

    # ---------------------------------------------------------------- stop rules

    def test_s4_with_pickable_hypothesis(self):
        stop = dict(BASE_STOP, rule="S4")
        self.assertFails(self.build(stop=stop), "stop_reason_s4_violated")

    def test_s4_when_exhausted_passes(self):
        # H3 born on C1, seen on C2 and C3, already tested on EXPLORE -> nothing left: S4 is right.
        beliefs = base_beliefs()
        beliefs["H3"].update(born_on="C1 cell_03", seen_on="C2, C3", posterior=0.462)
        cells = base_cells()
        cells[5] = ("H3", "EXPLORE", "test", "supported", 2)
        cells[6] = ("H1", "VAL", "val", "supported", 10)
        stop = dict(BASE_STOP, rule="S4")
        report = self.build(beliefs=beliefs, cells=cells, stop=stop)
        self.assertTrue(report.ok, [f"{i.code}: {i.message}" for i in report.issues])

    def test_s2_with_nothing_left_is_s4(self):
        beliefs = base_beliefs()
        beliefs["H3"].update(born_on="C1 cell_03", seen_on="C2, C3", posterior=0.462)
        cells = base_cells()
        cells[5] = ("H3", "EXPLORE", "test", "supported", 2)
        cells[6] = ("H1", "VAL", "val", "supported", 10)
        self.assertFails(self.build(beliefs=beliefs, cells=cells), "stop_reason_s2_no_tests")

    def test_s1_with_open_entry(self):
        stop = dict(BASE_STOP, rule="S1")
        self.assertFails(self.build(stop=stop), "stop_reason_s1_violated")

    def test_count_mismatch(self):
        stop = dict(BASE_STOP, open_count=2)
        self.assertFails(self.build(stop=stop), "stop_reason_count_mismatch")

    # ---------------------------------------------------------------- headers

    def test_rule_without_header(self):
        report = self.build()
        rule = os.path.join(report.run_dir, "cells", "cell_01_rule.md")
        write(rule, "# rule with no header\n")
        self.assertFails(gate.check_run(report.run_dir), "cell_rule_no_header")

    # ---------------------------------------------------------------- v3.2: mode

    def test_missing_mode_line(self):
        report = self.build()
        write(os.path.join(report.run_dir, "DECISIONS.md"), "# DECISIONS\nno mode here\n")
        self.assertFails(gate.check_run(report.run_dir), "decisions_no_mode")

    # ---------------------------------------------------------------- v3.2: installs

    INSTALL_ROW = ("| import | package | version | source | claim | replaces | adds | validation | result |\n"
                   "|---|---|---|---|---|---|---|---|---|\n"
                   "| ruptures | ruptures | 1.1.9 | pypi | H1 break date | rolling-mean eyeballing | "
                   "penalised change-point search | cells/install_ruptures.md | PASS |\n")

    def test_base_imports_need_no_row(self):
        files = {"scripts/cell_01.py": "import numpy as np\nfrom scipy import stats\nimport json, os\nimport common\n",
                 "scripts/common.py": "import pandas as pd\n"}
        report = self.build(files=files)
        self.assertTrue(report.ok, [f"{i.code}: {i.message}" for i in report.issues])

    def test_unlogged_install(self):
        self.assertFails(self.build(files={"scripts/cell_01.py": "import ruptures as rpt\n"}), "install_unlogged")

    def test_logged_and_validated_install_passes(self):
        files = {"scripts/cell_01.py": "import ruptures as rpt\n", "INSTALLS.md": self.INSTALL_ROW,
                 "cells/install_ruptures.md": "planted break at 5000 found at 5000\n"}
        report = self.build(files=files)
        self.assertTrue(report.ok, [f"{i.code}: {i.message}" for i in report.issues])

    def test_install_unpinned_bad_source_failed_validation(self):
        row = self.INSTALL_ROW.replace("1.1.9", "latest").replace("| pypi |", "| github |").replace("| PASS |", "| FAIL |")
        files = {"scripts/cell_01.py": "import ruptures\n", "INSTALLS.md": row,
                 "cells/install_ruptures.md": "x\n"}
        report = self.build(files=files)
        for code in ("install_unpinned", "install_bad_source", "install_validation_failed"):
            self.assertFails(report, code)

    def test_install_without_validation_file_or_reason(self):
        row = self.INSTALL_ROW.replace("penalised change-point search", "-")
        files = {"scripts/cell_01.py": "from ruptures import Pelt\n", "INSTALLS.md": row}
        report = self.build(files=files)
        self.assertFails(report, "install_no_validation")
        self.assertFails(report, "install_no_reason")

    # ---------------------------------------------------------------- v3.2: method fidelity (modes B/C)

    SPEC = """# METHOD_SPEC
## M1 — Fama-MacBeth slope on 1-month reversal
source: Jegadeesh 1990, section II
estimator: cross-sectional OLS each month, time-series mean of slopes, NW(6) t
library: statsmodels OLS + linearmodels.FamaMacBeth
parameters: lookback 1 month, skip 0, monthly rebalance
sample: monthly, all coins with 12 months history
match: deviation
deviation_reason: paper uses CRSP stocks; we have 10 coins, so the cross-section is 10 wide
"""

    def source_beliefs(self):
        b = base_beliefs()
        b["H1"]["born_on"] = "SOURCE Jegadeesh 1990"
        return b

    def test_mode_b_requires_method_spec(self):
        self.assertFails(self.build(beliefs=self.source_beliefs(), mode="B"), "method_spec_missing")

    def test_mode_b_source_hypothesis_must_cite_method(self):
        report = self.build(beliefs=self.source_beliefs(), mode="B", files={"METHOD_SPEC.md": self.SPEC})
        self.assertFails(report, "method_not_used")

    def test_mode_b_with_cited_method_passes(self):
        cells = base_cells()
        cells[1] = ("H1", "C1", "test", "supported", 10, "M1")
        report = self.build(beliefs=self.source_beliefs(), cells=cells, mode="B", files={"METHOD_SPEC.md": self.SPEC})
        self.assertTrue(report.ok, [f"{i.code}: {i.message}" for i in report.issues])

    def test_unexplained_deviation_and_unknown_method(self):
        spec = self.SPEC.replace("deviation_reason: paper uses CRSP stocks; we have 10 coins, so the cross-section is 10 wide",
                                 "deviation_reason: none")
        cells = base_cells()
        cells[1] = ("H1", "C1", "test", "supported", 10, "M1")
        cells[2] = ("H1", "C2", "test", "supported", 10, "M7")
        report = self.build(beliefs=self.source_beliefs(), cells=cells, mode="C", files={"METHOD_SPEC.md": spec})
        self.assertFails(report, "method_deviation_unexplained")
        self.assertFails(report, "method_unknown_ref")

    # ---------------------------------------------------------------- v3.2: memory

    def test_memory_file_missing(self):
        self.assertFails(self.build(memory={"DATA_FACTS.md": None}), "memory_missing")

    def test_ledger_row_missing(self):
        self.assertFails(self.build(memory={"LEDGER.md": LEDGER_HEAD}), "ledger_row_missing")

    def test_ledger_k_below_scored_openings(self):
        mem = memory_files(base_beliefs(), base_cells(), k=1)
        self.assertFails(self.build(memory={"LEDGER.md": mem["LEDGER.md"]}), "ledger_k_too_small")

    def test_ledger_kcum_carries_dataset_history(self):
        prior = "| 2025-12-01 | old_run | t | E | S4 | 9 | 7 | ds1 | 7 | 2 |\n"
        good = memory_files(base_beliefs(), base_cells(), k=4, k_cum=11, prior_rows=prior)["LEDGER.md"]
        bad = memory_files(base_beliefs(), base_cells(), k=4, k_cum=4, prior_rows=prior)["LEDGER.md"]
        self.assertTrue(self.build(memory={"LEDGER.md": good}).ok)
        self.assertFails(self.build(memory={"LEDGER.md": bad}), "ledger_bad_kcum")

    def test_ledger_bad_score(self):
        mem = memory_files(base_beliefs(), base_cells(), score="great")
        self.assertFails(self.build(memory={"LEDGER.md": mem["LEDGER.md"]}), "ledger_bad_score")

    def test_findings_entry_missing_low_line_missing(self):
        self.assertFails(self.build(memory={"FINDINGS.md": "# FINDINGS\n"}), "findings_missing")
        self.assertFails(self.build(memory={"FINDINGS.md": "# FINDINGS\n"}), "findings_low_line_missing")

    def test_findings_entry_too_long(self):
        mem = memory_files(base_beliefs(), base_cells())["FINDINGS.md"]
        mem = mem.replace("needs: nothing\n", "needs: nothing\nline 3\nline 4\n")
        self.assertFails(self.build(memory={"FINDINGS.md": mem}), "findings_too_long")

    def test_memory_over_budget(self):
        facts = "# DATA_FACTS\n" + "".join(f"- ds1: fact {i}\n" for i in range(200))
        self.assertFails(self.build(memory={"DATA_FACTS.md": facts}), "memory_over_budget")


if __name__ == "__main__":
    unittest.main()
