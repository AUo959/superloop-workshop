"""Invariant, determinism, and comparison tests for E001 Stage A."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from superloop_e001.model import TRACE_FIELDS
from superloop_e001.simulator import matrix_manifest, run_matrix, run_simulation
from superloop_e001.workloads import CONFIGURATIONS, SCENARIOS, SEEDS, build_offers
from tools.generate_e001_evidence import generate


class E001SimulatorTests(unittest.TestCase):
    def test_frozen_matrix_dimensions(self) -> None:
        self.assertEqual(3, len(CONFIGURATIONS))
        self.assertEqual(8, len(SCENARIOS))
        self.assertEqual(3, len(SEEDS))
        self.assertEqual(40, len(build_offers("balanced")))
        self.assertEqual(64, len(build_offers("burst")))
        self.assertEqual(48, len(build_offers("saturated_receiver")))
        self.assertEqual(42, len(build_offers("malformed_duplicate")))
        matrix_path = (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "E001"
            / "config"
            / "CANONICAL_MATRIX__E001__v0.1__2026-07-13.json"
        )
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
        self.assertEqual(list(CONFIGURATIONS), matrix["configurations"])
        self.assertEqual(list(SCENARIOS), matrix["scenarios"])
        self.assertEqual(list(SEEDS), matrix["seeds"])
        self.assertEqual(8, matrix["parameters"]["capacity_per_loop"])
        self.assertEqual(3, matrix["parameters"]["credit_lease_ticks"])
        self.assertEqual(60, matrix["parameters"]["work_deadline_ticks"])
        self.assertEqual(240, matrix["parameters"]["primary_horizon"])
        self.assertEqual(360, matrix["parameters"]["maximum_drain_horizon"])

    def test_trace_is_byte_deterministic(self) -> None:
        first = run_simulation("local_cbf", "burst", 17)
        second = run_simulation("local_cbf", "burst", 17)
        self.assertEqual(first.trace_jsonl, second.trace_jsonl)
        self.assertEqual(first.summary["trace_digest"], second.summary["trace_digest"])
        self.assertEqual(first.summary["summary_digest"], second.summary["summary_digest"])

    def test_trace_records_have_exact_required_keys(self) -> None:
        result = run_simulation("local_cbf", "balanced", 17)
        self.assertTrue(result.trace)
        for event in result.trace:
            self.assertEqual(set(TRACE_FIELDS), set(event))
            json.dumps(event, sort_keys=True)

    def test_full_matrix_preserves_hard_invariants_and_equivalent_work(self) -> None:
        results = run_matrix()
        manifest = matrix_manifest(results)
        self.assertEqual(72, len(results))
        self.assertEqual(72, manifest["run_count"])
        self.assertEqual({}, manifest["workload_equivalence_mismatches"])
        self.assertEqual([], manifest["invalid_run_ids"])
        for result in results:
            summary = result.summary
            self.assertEqual(0, summary["invariant_violation_count"], summary["run_id"])
            self.assertEqual(0, summary["active_at_end"], summary["run_id"])
            self.assertLessEqual(max(summary["maximum_occupancy"].values()), 8)
            self.assertEqual(0, summary["final_unresolved_obligations"])
            self.assertEqual(0, summary["stale_authorization_count"])
            self.assertEqual(0, summary["duplicate_promotion_count"])
            self.assertEqual(100.0, summary["provenance_completeness_percent"])

    def test_stale_feedback_is_rejected(self) -> None:
        result = run_simulation("local_cbf", "stale_feedback", 29)
        self.assertEqual(1, result.summary["stale_rejection_count"])
        self.assertEqual(0, result.summary["stale_authorization_count"])
        stale_events = [
            event for event in result.trace if event["validation_state"] == "rejected_stale"
        ]
        self.assertEqual(1, len(stale_events))

    def test_malformed_and_duplicate_offers_do_not_promote(self) -> None:
        result = run_simulation("local_cbf", "malformed_duplicate", 43)
        terminals = result.summary["terminal_counts"]
        self.assertEqual(1, terminals["rejected_invalid"])
        self.assertEqual(1, terminals["duplicate_ignored"])
        self.assertEqual(0, result.summary["duplicate_promotion_count"])

    def test_circular_wait_terminates_accountably(self) -> None:
        central = run_simulation("central", "circular_wait", 17)
        barrier = run_simulation("global_barrier", "circular_wait", 17)
        local = run_simulation("local_cbf", "circular_wait", 17)
        for result in (central, barrier, local):
            self.assertEqual(24, result.summary["admitted"])
            self.assertEqual(0, result.summary["active_at_end"])
        self.assertEqual(24, central.summary["completed"])
        self.assertEqual(24, barrier.summary["completed"])
        self.assertEqual(24, local.summary["terminal_counts"]["expired_deadline"])
        self.assertEqual(0, local.summary["completed"])

    def test_offer_and_admission_ledgers_balance(self) -> None:
        for result in run_matrix():
            summary = result.summary
            rejected = sum(
                summary["terminal_counts"].get(state, 0)
                for state in ("rejected_invalid", "rejected_capacity", "duplicate_ignored")
            )
            self.assertEqual(summary["offered"], summary["admitted"] + rejected)

    def test_execution_metadata_is_separate_from_canonical_summary(self) -> None:
        result = run_simulation("local_cbf", "balanced", 17)
        self.assertNotIn("execution", result.summary)
        self.assertEqual(result.summary["run_id"], result.execution["run_id"])

    def test_every_transfer_commit_has_one_receipt(self) -> None:
        result = run_simulation("local_cbf", "burst", 17)
        commits = [event for event in result.trace if event["event_type"] == "transfer_commit"]
        receipts = [event for event in result.trace if event["event_type"] == "receipt"]
        self.assertEqual(len(commits), len(receipts))
        receipt_parents = [event["parent_event_ids"] for event in receipts]
        self.assertCountEqual([[event["event_id"]] for event in commits], receipt_parents)

    def test_local_interlocks_preserve_fault_locality_signal(self) -> None:
        global_barrier = run_simulation("global_barrier", "failed_neighbor", 17)
        local_cbf = run_simulation("local_cbf", "failed_neighbor", 17)
        self.assertGreaterEqual(
            local_cbf.summary["healthy_progress_ticks"],
            global_barrier.summary["healthy_progress_ticks"],
        )
        self.assertLessEqual(
            local_cbf.summary["fault_radius"],
            global_barrier.summary["fault_radius"],
        )

    def test_central_trace_accounts_for_work_blocked_by_failed_neighbor(self) -> None:
        result = run_simulation("central", "failed_neighbor", 17)
        blocked_transfer_waits = [
            event
            for event in result.trace
            if event["event_type"] == "wait"
            and event["interlock_id"] == "AB"
            and 40 <= event["simulation_tick"] <= 79
        ]
        self.assertTrue(blocked_transfer_waits)

    def test_evidence_generator_repeats_and_records_provenance(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            output = Path(directory) / "evidence"
            provenance = generate(output, "test-source-commit")
            self.assertEqual(72, provenance["validation"]["run_count"])
            self.assertEqual([], provenance["validation"]["determinism_mismatches"])
            self.assertEqual([], provenance["validation"]["invalid_run_ids"])
            self.assertEqual(
                {},
                provenance["validation"]["workload_equivalence_mismatches"],
            )
            self.assertEqual(72, len(list((output / "raw").glob("*.jsonl"))))
            self.assertEqual(72, len(list((output / "summary").glob("*.json"))))


if __name__ == "__main__":
    unittest.main()
