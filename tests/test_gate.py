"""Tests for gate.py. Run: python -m unittest discover -s tests

Each test builds a small, synthetic v3.3 run folder that passes the gate, breaks one rule, and checks
the gate names that rule. The run is not real data - only the files gate.py reads. File mtimes are set
explicitly (candidates first, then each cell's rule, then its result) so ordering checks are deterministic.
Posteriors are computed from the cells' weights unless a test gives one, so a test only states what it breaks.
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

T0 = 1_700_000_000


def belief(hid, title, born_on, state, prior, posterior, parent="none", forbids="a positive IC on the next fold"):
    return f"""## {hid} — {title}
parent: {parent}
source: OBSERVATIONS.md #1
question: does it?
hypothesis: a change in close predicts the next block because of a reason
forbids: {forbids}
rivals: volatility; time of day
born_on: {born_on}
prior: {prior}
anchor: uninformative default 0.4
posterior: {posterior:.4f}
state: {state}
"""


def candidate(hypothesis, variant_of="none"):
    return f"""hypothesis: {hypothesis}
variant_of: {variant_of}
spec: fade the 6h block return, IC on next 6h, 10-coin panel
construction: point-in-time inputs; trailing 30d z-score; winsorised 1/99; raw and market-neutral; market corr reported
pass_rule: supported if IC <= -0.02 and z <= -1.645; refuted if IC >= 0; else inconclusive
min_useful: |IC| 0.02
cost_line: IC -0.03 = 12 bp per 1-sd block vs 6.6 bp round trip -> STANDALONE
"""


def base_beliefs():
    # H1 searched, frozen as F1, held on CONFIRM, passed VAL -> CHECKED. H2 searched three ways, dropped.
    # H3 (child of H2, suggested by cell_05) still OPEN.
    return {
        "H1": dict(title="6h reversal", born_on="EXPLORE #1", state="CHECKED", prior=0.40),
        "H2": dict(title="daily reversal", born_on="EXPLORE #2", state="DROPPED", prior=0.30),
        "H3": dict(title="crash rebound", born_on="C2 cell_05", state="OPEN", parent="H2", prior=0.30),
    }


def base_candidates():
    return {"F1": candidate("H1")}


def base_cells():
    # nn: dict(h, slice, kind, w, ...); kind-specific: variants / controls / conditional / suggests / candidate / folds / branch
    return {
        1: dict(h="H1", slice="EXPLORE", kind="search", w=2, variants=12),
        2: dict(h="H1", slice="TRAIN", kind="search", w=2, variants=30, controls="trailing volatility"),
        3: dict(h="H2", slice="C1", kind="search", w=0.5, variants=5, controls="trailing volatility"),
        4: dict(h="H2", slice="TRAIN", kind="search", w=0.5, variants=4, conditional="high-vol regime only"),
        5: dict(h="H2", slice="C2", kind="search", w=0.5, variants=3, suggests="H3"),
        6: dict(h="H1", slice="CONFIRM", kind="confirm", w=10, candidate="F1",
                folds="C1=supported, C2=supported, C3=inconclusive"),
        7: dict(h="H1", slice="VAL", kind="val", w=10, candidate="F1", branch="supported"),
    }


def posterior_of(hid, prior, cells):
    odds = prior / (1 - prior)
    for c in cells.values():
        if c["h"] == hid:
            odds *= c["w"]
    return odds / (1 + odds)


BASE_STOP = dict(rule="S3", open_count=1, dropped_count=1, frozen_count=1, val_pass_count=1, minutes=185,
                 detail="185 minutes elapsed")


def write(path, text, mtime=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    if mtime is not None:
        os.utime(path, (mtime, mtime))


RUN = "2026-01-01_test"
LEDGER_HEAD = ("| date | run | target | mode | stop | cells | K_train | K_val | dataset | K_cum_train | K_cum_val | methods_score |\n"
               "|---|---|---|---|---|---|---|---|---|---|---|---|\n")


def k_of(cells):
    k_train = sum(c.get("variants", 0) for c in cells.values() if c["kind"] == "search")
    k_train += sum(1 for c in cells.values() if c["kind"] == "confirm")
    return k_train, sum(1 for c in cells.values() if c["kind"] == "val")


def ledger_row(cells, mode="E", k=None, k_cum=None, score="pending"):
    k = k or k_of(cells)
    k_cum = k_cum or k
    return (f"| 2026-01-01 | {RUN} | test | {mode} | S3 | {len(cells)} | {k[0]} | {k[1]} | ds1 | "
            f"{k_cum[0]} | {k_cum[1]} | {score} |\n")


FINDINGS = f"# FINDINGS\n\n- {RUN} DROPPED: H2\n\n### {RUN} F1 — 6h reversal\nclaim\nVAL-PASS\n\n"


def memory_files(cells, mode="E"):
    """Valid MEMORY/ contents for a run: one LEDGER row, a FINDINGS entry for F1, a DROPPED line, a DATA_FACTS file."""
    return {"LEDGER.md": LEDGER_HEAD + ledger_row(cells, mode), "FINDINGS.md": FINDINGS,
            "DATA_FACTS.md": "# DATA_FACTS\n- ds1: fact\n"}


class GateTest(unittest.TestCase):
    def build(self, beliefs=None, cells=None, cands=None, stop=None, splits=SPLITS, mode="E", memory=None,
              files=None, test_requests=None, decisions=None):
        """Synthetic run at <tmp>/runs/<RUN> with its MEMORY at <tmp>/MEMORY (gate's default location).
        `memory` overrides individual MEMORY files; `files` adds or replaces files in the run folder."""
        beliefs = beliefs if beliefs is not None else base_beliefs()
        cells = cells if cells is not None else base_cells()
        cands = cands if cands is not None else base_candidates()
        stop = stop if stop is not None else BASE_STOP
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        d = os.path.join(tmp.name, "runs", RUN)
        os.makedirs(d)
        for name in gate.REQUIRED_FILES:
            write(os.path.join(d, name), f"# {name}\n")
        if decisions is None:
            decisions = "".join(f"- drop {h}: nothing survived three looks\n" for h, kw in beliefs.items()
                                if kw["state"] == "DROPPED")
        write(os.path.join(d, "DECISIONS.md"), f"# DECISIONS\nmode: {mode}\n{decisions}")
        mem = memory_files(cells, mode)
        mem.update(memory or {})
        for name, text in mem.items():
            if text is not None:
                write(os.path.join(tmp.name, "MEMORY", name), text)
        write(os.path.join(d, "DATA_PROFILE.md"), "".join(f"## {i}. section\n" for i in range(1, 8)))
        write(os.path.join(d, "SPLITS.md"), splits)
        blocks = []
        for h, kw in beliefs.items():
            kw = dict(kw)
            kw.setdefault("posterior", posterior_of(h, kw["prior"], cells))
            blocks.append(belief(h, **kw))
        write(os.path.join(d, "BELIEFS.md"), "# BELIEFS\n\n" + "\n".join(blocks))
        write(os.path.join(d, "STOP_REASON.md"), "".join(f"{k}: {v}\n" for k, v in stop.items()))
        shas = {}
        for fid, text in cands.items():
            p = os.path.join(d, "candidates", f"{fid}.md")
            write(p, text, T0)
            shas[fid] = gate.sha256_of(p)
        os.makedirs(os.path.join(d, "cells"))
        for nn, c in cells.items():
            p = os.path.join(d, "cells", f"cell_{nn:02d}_")
            head = f"hypothesis: {c['h']}\nslice: {c['slice']}\nkind: {c['kind']}\n"
            if c.get("candidate"):
                head += f"candidate: {c['candidate']}\n"
            if c["kind"] == "val":
                head += f"spec_sha256: {c.get('sha', shas.get(c.get('candidate'), 'x'))}\n"
            if c.get("method"):
                head += f"method: {c['method']}\n"
            if c["kind"] == "search":
                head += f"controls: {c.get('controls', 'none')}\nconditional: {c.get('conditional', 'none')}\n"
            res = f"weight_applied: {c['w']}\n"
            if c["kind"] == "search":
                res += f"variants: {c.get('variants', 1)}\nsuggests: {c.get('suggests', 'none')}\n"
            elif c["kind"] == "confirm":
                res += f"folds: {c['folds']}\n"
            else:
                res += f"branch: {c['branch']}\n"
            write(p + "rule.md", head + "\n# rule\n", T0 + 100 * nn)
            write(p + "announce.md", "# announce\n", T0 + 100 * nn)
            write(p + "result.md", res + "\n# result\n", T0 + 100 * nn + 50)
        if test_requests is None:
            test_requests = "".join(f"## {f}\nspec_sha256: {s}\nlabel: STANDALONE\n" for f, s in shas.items())
        write(os.path.join(d, "TEST_REQUESTS.md"), "# TEST_REQUESTS\n" + test_requests)
        for name, text in (files or {}).items():
            write(os.path.join(d, name), text)
        return gate.check_run(d)

    def codes(self, report):
        return {i.code for i in report.issues}

    def assertFails(self, report, code):
        self.assertIn(code, self.codes(report), [f"{i.code}: {i.message}" for i in report.issues])

    def assertPasses(self, report):
        self.assertTrue(report.ok, [f"{i.code}: {i.message}" for i in report.issues])

    def with_ledger(self, cells):
        return {"LEDGER.md": LEDGER_HEAD + ledger_row(cells)}

    # ---------------------------------------------------------------- the baseline

    def test_baseline_passes(self):
        self.assertPasses(self.build())

    # ---------------------------------------------------------------- splits

    def test_one_fold_is_too_few(self):
        splits = SPLITS.replace("- C2 2022-01-08 2022-07-01\n", "").replace("- C3 2022-07-08 2023-03-20\n", "")
        self.assertFails(self.build(splits=splits), "splits_too_few_folds")

    def test_missing_slices_block(self):
        self.assertFails(self.build(splits="# SPLITS\nEXPLORE then CONFIRM\n"), "splits_no_block")

    def test_overlapping_folds(self):
        splits = SPLITS.replace("- C2 2022-01-08", "- C2 2021-12-01")
        self.assertFails(self.build(splits=splits), "splits_overlap")

    # ---------------------------------------------------------------- search is free on TRAIN, never on VAL

    def test_search_repeats_any_train_slice(self):
        cells = base_cells()
        cells[8] = dict(h="H3", slice="C2", kind="search", w=1.5, variants=4)   # its own birth slice: fine
        cells[9] = dict(h="H3", slice="C2", kind="search", w=1.5, variants=4)   # the same slice again: fine
        cells[10] = dict(h="H3", slice="C1, C2", kind="search", w=1, variants=2)
        self.assertPasses(self.build(cells=cells, memory=self.with_ledger(cells)))

    def test_search_on_val(self):
        cells = base_cells()
        cells[5]["slice"] = "C3, VAL"
        self.assertFails(self.build(cells=cells), "search_on_val")

    def test_born_on_val(self):
        beliefs = base_beliefs()
        beliefs["H3"]["born_on"] = "VAL cell_07"
        self.assertFails(self.build(beliefs=beliefs), "beliefs_bad_born_on")

    def test_search_needs_variants(self):
        cells = base_cells()
        cells[1]["variants"] = 0
        self.assertFails(self.build(cells=cells), "cell_result_no_variants")

    # ---------------------------------------------------------------- prior -> posterior updating

    def test_missing_prior(self):
        report = self.build()
        p = os.path.join(report.run_dir, "BELIEFS.md")
        with open(p, encoding="utf-8") as fh:
            text = fh.read().replace("prior: 0.3\n", "", 1)
        write(p, text)
        self.assertFails(gate.check_run(report.run_dir), "beliefs_missing_fields")

    def test_posterior_mismatch(self):
        beliefs = base_beliefs()
        beliefs["H1"]["posterior"] = 0.60
        self.assertFails(self.build(beliefs=beliefs), "posterior_mismatch")

    def test_search_weight_capped_at_3(self):
        cells = base_cells()
        cells[1]["w"] = 5
        self.assertFails(self.build(cells=cells), "weight_over_cap")

    def test_check_weight_capped_at_10(self):
        cells = base_cells()
        cells[7]["w"] = 20
        self.assertFails(self.build(cells=cells), "weight_over_cap")

    def test_missing_weight(self):
        report = self.build()
        write(os.path.join(report.run_dir, "cells", "cell_01_result.md"), "variants: 12\nsuggests: none\n", T0 + 150)
        self.assertFails(gate.check_run(report.run_dir), "cell_result_no_weight")

    # ---------------------------------------------------------------- no lazy drops, every lead answered

    def test_drop_after_one_look(self):
        cells = base_cells()
        del cells[4], cells[5]
        beliefs = base_beliefs()
        beliefs["H3"]["born_on"] = "C1 cell_03"
        self.assertFails(self.build(cells=cells, beliefs=beliefs, memory=self.with_ledger(cells)), "drop_too_early")

    def test_drop_without_rival_controlled(self):
        cells = base_cells()
        cells[3]["controls"] = "none"
        self.assertFails(self.build(cells=cells), "drop_no_rival_controlled")

    def test_drop_without_conditional(self):
        cells = base_cells()
        cells[4]["conditional"] = "none"
        self.assertFails(self.build(cells=cells), "drop_no_conditional")

    def test_drop_with_posterior_up(self):
        cells = base_cells()
        for nn in (3, 4, 5):
            cells[nn]["w"] = 1.5
        self.assertFails(self.build(cells=cells), "drop_posterior_not_down")

    def test_drop_without_reason(self):
        self.assertFails(self.build(decisions=""), "drop_no_reason")

    def test_search_needs_suggests(self):
        report = self.build()
        write(os.path.join(report.run_dir, "cells", "cell_01_result.md"), "weight_applied: 2\nvariants: 12\n", T0 + 150)
        self.assertFails(gate.check_run(report.run_dir), "cell_result_no_suggests")

    def test_suggests_unknown_hypothesis(self):
        cells = base_cells()
        cells[5]["suggests"] = "H3, H9"
        self.assertFails(self.build(cells=cells), "suggests_unknown_hypothesis")

    # ---------------------------------------------------------------- freezing and CONFIRM

    def test_check_without_candidate_file(self):
        self.assertFails(self.build(cands={}), "check_no_candidate")

    def test_spec_edited_after_check_set_up(self):
        report = self.build()
        os.utime(os.path.join(report.run_dir, "candidates", "F1.md"), (T0 + 1000, T0 + 1000))
        self.assertFails(gate.check_run(report.run_dir), "check_spec_not_frozen")

    def test_confirm_must_name_every_fold(self):
        cells = base_cells()
        cells[6]["folds"] = "C1=supported, C2=supported"
        self.assertFails(self.build(cells=cells), "cell_result_bad_folds")

    def test_confirm_twice(self):
        cells = base_cells()
        cells[8], cells[7] = cells[7], dict(cells[6], w=1)
        self.assertFails(self.build(cells=cells), "confirm_twice")

    def test_frozen_but_never_confirmed(self):
        cands = base_candidates()
        cands["F2"] = candidate("H3")
        self.assertFails(self.build(cands=cands, stop=dict(BASE_STOP, frozen_count=2)), "confirm_owed")

    # ---------------------------------------------------------------- VAL

    def test_val_after_failed_confirm(self):
        cells = base_cells()
        cells[6]["folds"] = "C1=supported, C2=refuted, C3=supported"
        self.assertFails(self.build(cells=cells), "val_not_confirm_shown")

    def test_val_without_confirm(self):
        cells = base_cells()
        del cells[6]
        self.assertFails(self.build(cells=cells), "val_not_confirm_shown")

    def test_val_spec_changed(self):
        cells = base_cells()
        cells[7]["sha"] = "0" * 64
        self.assertFails(self.build(cells=cells), "val_spec_mismatch")

    def test_val_twice_on_same_spec(self):
        cells = base_cells()
        cells[8] = dict(cells[7], w=1)
        self.assertFails(self.build(cells=cells), "val_twice")

    def test_confirm_shown_without_val(self):
        cells = base_cells()
        del cells[7]
        beliefs = base_beliefs()
        beliefs["H1"]["state"] = "OPEN"
        stop = dict(BASE_STOP, open_count=2, val_pass_count=0)
        self.assertFails(self.build(beliefs=beliefs, cells=cells, stop=stop), "val_owed")

    def test_variant_after_val_fail_passes(self):
        # F1 fails VAL; back to TRAIN search; F2 (variant of F1) frozen, confirmed, checked on VAL and passes.
        cells = base_cells()
        cells[7].update(branch="refuted", w=0.2)
        cells[8] = dict(h="H1", slice="TRAIN", kind="search", w=1, variants=8)
        cells[9] = dict(h="H1", slice="CONFIRM", kind="confirm", w=5, candidate="F2",
                        folds="C1=supported, C2=supported, C3=supported")
        cells[10] = dict(h="H1", slice="VAL", kind="val", w=10, candidate="F2", branch="supported")
        cands = base_candidates()
        cands["F2"] = candidate("H1", variant_of="F1")
        memory = self.with_ledger(cells)
        memory["FINDINGS.md"] = FINDINGS + f"### {RUN} F2 — variant\nx\n"
        self.assertPasses(self.build(cells=cells, cands=cands, stop=dict(BASE_STOP, frozen_count=2), memory=memory))

    def test_bad_variant_of(self):
        self.assertFails(self.build(cands={"F1": candidate("H1", variant_of="F9")}), "candidate_bad_variant_of")

    # ---------------------------------------------------------------- TEST is handed to the user

    def test_val_pass_not_requested(self):
        self.assertFails(self.build(test_requests=""), "test_request_missing")

    def test_test_request_wrong_sha(self):
        self.assertFails(self.build(test_requests="## F1\nspec_sha256: abc\n"), "test_request_bad_sha")

    def test_test_request_needs_label(self):
        report = self.build()
        sha = gate.sha256_of(os.path.join(report.run_dir, "candidates", "F1.md"))
        write(os.path.join(report.run_dir, "TEST_REQUESTS.md"), f"## F1\nspec_sha256: {sha}\nlabel: maybe\n")
        self.assertFails(gate.check_run(report.run_dir), "test_request_no_label")

    def test_candidate_needs_construction(self):
        self.assertFails(self.build(cands={"F1": candidate("H1").replace("construction:", "notes:")}),
                         "candidate_missing_fields")

    # ---------------------------------------------------------------- states and stop rules

    def test_checked_without_val(self):
        beliefs = base_beliefs()
        beliefs["H3"]["state"] = "CHECKED"
        self.assertFails(self.build(beliefs=beliefs, stop=dict(BASE_STOP, open_count=0)), "state_mismatch")

    def test_s1_with_open_entry(self):
        self.assertFails(self.build(stop=dict(BASE_STOP, rule="S1")), "stop_reason_s1_violated")

    def test_s1_too_early(self):
        beliefs = base_beliefs()
        del beliefs["H3"]
        cells = base_cells()
        cells[5]["suggests"] = "not pursued: no mechanism"
        stop = dict(BASE_STOP, rule="S1", open_count=0, minutes=40)
        self.assertFails(self.build(beliefs=beliefs, cells=cells, stop=stop), "stop_reason_s1_too_early")

    def test_s1_after_floor_passes(self):
        beliefs = base_beliefs()
        del beliefs["H3"]
        cells = base_cells()
        cells[5]["suggests"] = "not pursued: no mechanism"
        stop = dict(BASE_STOP, rule="S1", open_count=0, minutes=95)
        self.assertPasses(self.build(beliefs=beliefs, cells=cells, stop=stop))

    def test_s3_under_cap(self):
        self.assertFails(self.build(stop=dict(BASE_STOP, minutes=30)), "stop_reason_s3_under_cap")

    def test_s2_needs_a_dry_streak(self):
        self.assertFails(self.build(stop=dict(BASE_STOP, rule="S2")), "stop_reason_s2_violated")

    def test_s2_with_dry_streak_passes(self):
        cells = base_cells()
        for nn in range(8, 8 + gate.DRY_STREAK):
            cells[nn] = dict(h="H3", slice="TRAIN", kind="search", w=1, variants=3)
        self.assertPasses(self.build(cells=cells, stop=dict(BASE_STOP, rule="S2"), memory=self.with_ledger(cells)))

    def test_count_mismatch(self):
        self.assertFails(self.build(stop=dict(BASE_STOP, open_count=2)), "stop_reason_count_mismatch")

    # ---------------------------------------------------------------- headers

    def test_rule_without_header(self):
        report = self.build()
        write(os.path.join(report.run_dir, "cells", "cell_01_rule.md"), "# rule with no header\n", T0 + 100)
        self.assertFails(gate.check_run(report.run_dir), "cell_rule_no_header")

    def test_result_before_rule(self):
        report = self.build()
        os.utime(os.path.join(report.run_dir, "cells", "cell_02_result.md"), (T0, T0))
        self.assertFails(gate.check_run(report.run_dir), "cell_result_before_rule")

    # ---------------------------------------------------------------- mode

    def test_missing_mode_line(self):
        report = self.build()
        write(os.path.join(report.run_dir, "DECISIONS.md"), "# DECISIONS\nno mode here\n- drop H2: x\n")
        self.assertFails(gate.check_run(report.run_dir), "decisions_no_mode")

    # ---------------------------------------------------------------- installs

    INSTALL_ROW = ("| import | package | version | source | claim | replaces | adds | validation | result |\n"
                   "|---|---|---|---|---|---|---|---|---|\n"
                   "| ruptures | ruptures | 1.1.9 | pypi | H1 break date | rolling-mean eyeballing | "
                   "penalised change-point search | cells/install_ruptures.md | PASS |\n")

    def test_base_imports_need_no_row(self):
        files = {"scripts/cell_01.py": "import numpy as np\nfrom scipy import stats\nimport json, os\nimport common\n",
                 "scripts/common.py": "import pandas as pd\n"}
        self.assertPasses(self.build(files=files))

    def test_unlogged_install(self):
        self.assertFails(self.build(files={"scripts/cell_01.py": "import ruptures as rpt\n"}), "install_unlogged")

    def test_logged_and_validated_install_passes(self):
        files = {"scripts/cell_01.py": "import ruptures as rpt\n", "INSTALLS.md": self.INSTALL_ROW,
                 "cells/install_ruptures.md": "planted break at 5000 found at 5000\n"}
        self.assertPasses(self.build(files=files))

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

    # ---------------------------------------------------------------- method fidelity (modes B/C)

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
        cells[1]["method"] = "M1"
        report = self.build(beliefs=self.source_beliefs(), cells=cells, mode="B", files={"METHOD_SPEC.md": self.SPEC})
        self.assertPasses(report)

    def test_unexplained_deviation_and_unknown_method(self):
        spec = self.SPEC.replace("deviation_reason: paper uses CRSP stocks; we have 10 coins, so the cross-section is 10 wide",
                                 "deviation_reason: none")
        cells = base_cells()
        cells[1]["method"] = "M1"
        cells[2]["method"] = "M7"
        report = self.build(beliefs=self.source_beliefs(), cells=cells, mode="C", files={"METHOD_SPEC.md": spec})
        self.assertFails(report, "method_deviation_unexplained")
        self.assertFails(report, "method_unknown_ref")

    # ---------------------------------------------------------------- memory

    def test_memory_file_missing(self):
        self.assertFails(self.build(memory={"DATA_FACTS.md": None}), "memory_missing")

    def test_ledger_row_missing(self):
        self.assertFails(self.build(memory={"LEDGER.md": LEDGER_HEAD}), "ledger_row_missing")

    def test_ledger_k_counts_every_variant(self):
        cells = base_cells()   # K_train = 12 + 30 + 5 + 4 + 3 + 1 confirm = 55
        self.assertFails(self.build(memory={"LEDGER.md": LEDGER_HEAD + ledger_row(cells, k=(7, 1))}), "ledger_k_too_small")

    def test_ledger_k_val_counted(self):
        cells = base_cells()
        self.assertFails(self.build(memory={"LEDGER.md": LEDGER_HEAD + ledger_row(cells, k=(55, 0))}), "ledger_k_too_small")

    def test_ledger_kcum_carries_dataset_history(self):
        cells = base_cells()
        prior = "| 2025-12-01 | old_run | t | E | S3 | 9 | 100 | 2 | ds1 | 100 | 2 | 2 |\n"
        good = LEDGER_HEAD + prior + ledger_row(cells, k_cum=(155, 3))
        bad = LEDGER_HEAD + prior + ledger_row(cells, k_cum=(155, 1))
        self.assertPasses(self.build(memory={"LEDGER.md": good}))
        self.assertFails(self.build(memory={"LEDGER.md": bad}), "ledger_bad_kcum")

    def test_ledger_bad_score(self):
        self.assertFails(self.build(memory={"LEDGER.md": LEDGER_HEAD + ledger_row(base_cells(), score="great")}),
                         "ledger_bad_score")

    def test_findings_entry_and_dropped_line_missing(self):
        report = self.build(memory={"FINDINGS.md": "# FINDINGS\n"})
        self.assertFails(report, "findings_missing")
        self.assertFails(report, "findings_line_missing")

    def test_findings_entry_too_long(self):
        mem = FINDINGS.replace("VAL-PASS\n", "VAL-PASS\nline 3\nline 4\n")
        self.assertFails(self.build(memory={"FINDINGS.md": mem}), "findings_too_long")

    def test_memory_over_budget(self):
        facts = "# DATA_FACTS\n" + "".join(f"- ds1: fact {i}\n" for i in range(200))
        self.assertFails(self.build(memory={"DATA_FACTS.md": facts}), "memory_over_budget")


if __name__ == "__main__":
    unittest.main()
