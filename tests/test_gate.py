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
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


class GateTest(unittest.TestCase):
    def build(self, beliefs=None, cells=None, stop=None, splits=SPLITS):
        beliefs = beliefs if beliefs is not None else base_beliefs()
        cells = cells if cells is not None else base_cells()
        stop = stop if stop is not None else BASE_STOP
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        d = tmp.name
        for name in gate.REQUIRED_FILES:
            write(os.path.join(d, name), f"# {name}\n")
        write(os.path.join(d, "DATA_PROFILE.md"), "".join(f"## {i}. section\n" for i in range(1, 8)))
        write(os.path.join(d, "SPLITS.md"), splits)
        write(os.path.join(d, "BELIEFS.md"), "# BELIEFS\n\n" + "\n".join(belief(h, **kw) for h, kw in beliefs.items()))
        write(os.path.join(d, "STOP_REASON.md"), "".join(f"{k}: {v}\n" for k, v in stop.items()))
        os.makedirs(os.path.join(d, "cells"))
        for nn, (hid, sl, kind, branch, weight) in cells.items():
            p = os.path.join(d, "cells", f"cell_{nn:02d}_")
            write(p + "rule.md", f"hypothesis: {hid}\nslice: {sl}\nkind: {kind}\n\n# rule\n")
            write(p + "announce.md", "# announce\n")
            write(p + "result.md", f"branch: {branch}\nweight_applied: {weight}\n\n# result\n")
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


if __name__ == "__main__":
    unittest.main()
