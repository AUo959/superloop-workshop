"""Tests for E002 exact-rational, offline trace instrumentation."""

from __future__ import annotations

import ast
import json
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from superloop_e002.model import auc, parse_rational, rational
from superloop_e002.replayer import (
    ARCHIVE_SHA256,
    TELEMETRY_FIELDS,
    EvidenceArchive,
    replay_archive,
    replay_run,
)


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = (
    ROOT
    / "experiments"
    / "E001"
    / "results"
    / "raw"
    / "E001__CANONICAL_EVIDENCE__81e7f859f71425bdba7603a61566f9fb47c116f9.tar.gz"
)


class E002ReplayerTests(unittest.TestCase):
    def test_exact_rational_encoding_and_auc(self) -> None:
        self.assertEqual({"numerator": 1, "denominator": 2}, rational(Fraction(2, 4)))
        self.assertEqual(Fraction(-1, 3), parse_rational({"numerator": -1, "denominator": 3}))
        self.assertEqual(
            Fraction(7, 8),
            auc(
                [
                    (Fraction(4), 1),
                    (Fraction(3), 1),
                    (Fraction(3), 0),
                    (Fraction(1), 0),
                ]
            ),
        )

    def test_archive_and_all_source_digests_verify(self) -> None:
        with EvidenceArchive(ARCHIVE) as archive:
            self.assertEqual(72, len(archive.run_ids))
            self.assertEqual(ARCHIVE_SHA256, __import__("hashlib").sha256(ARCHIVE.read_bytes()).hexdigest())
            for run_id in archive.run_ids:
                events, text, summary = archive.load_run(run_id)
                self.assertTrue(events)
                self.assertTrue(text.endswith("\n"))
                self.assertEqual(run_id, summary["run_id"])

    def test_one_run_reconstructs_and_is_byte_deterministic(self) -> None:
        with EvidenceArchive(ARCHIVE) as archive:
            events, _, summary = archive.load_run("local_cbf__failed_neighbor__seed-17")
        first, _ = replay_run(events, summary)
        second, _ = replay_run(events, summary)
        self.assertEqual(first, second)
        self.assertEqual("pass", first["reconstruction"]["status"])
        self.assertEqual(summary["occupancy_time"], first["reconstruction"]["occupancy_time"])
        self.assertTrue(all(value == "pass" for value in first["hard_invariants"].values()))

    def test_telemetry_schema_and_no_float_values(self) -> None:
        with EvidenceArchive(ARCHIVE) as archive:
            events, _, summary = archive.load_run("local_cbf__balanced__seed-17")
        from io import StringIO

        output = StringIO()
        run_summary, _ = replay_run(events, summary, output)
        records = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(run_summary["record_count"], len(records))
        self.assertTrue(records)
        for record in records:
            self.assertEqual(TELEMETRY_FIELDS, set(record))
            self._assert_no_float(record)
            if record["sample_phase"] == "pre_tick":
                self.assertTrue(
                    all(
                        int(event_id.rsplit(":", 1)[1])
                        < min(
                            [
                                int(event["event_id"].rsplit(":", 1)[1])
                                for event in events
                                if event["simulation_tick"] == record["simulation_tick"]
                            ]
                            or [10**9]
                        )
                        for event_id in record["source_event_ids"]
                    )
                )

    def test_typed_diagnostics_remain_distinct(self) -> None:
        from io import StringIO

        cases = {
            "local_cbf__circular_wait__seed-17": (0, "AB", "capacity", "blocked"),
            "local_cbf__failed_neighbor__seed-17": (40, "AB", "fault", "isolated"),
            "local_cbf__stale_feedback__seed-17": (30, "AB", "stale_authority", "rejected"),
        }
        with EvidenceArchive(ARCHIVE) as archive:
            for run_id, (tick, interlock, channel, expected) in cases.items():
                events, _, summary = archive.load_run(run_id)
                output = StringIO()
                replay_run(events, summary, output)
                matching = [
                    json.loads(line)
                    for line in output.getvalue().splitlines()
                    if f":{tick:03d}:post_tick:interlock:{interlock}" in line
                ]
                self.assertEqual(1, len(matching))
                diagnostic = matching[0]["reconstruction_state"]["diagnostic_states"]
                self.assertEqual(expected, diagnostic[channel]["state"])
                self.assertEqual(
                    {"capacity", "fault", "semantic_rejection", "stale_authority", "reciprocal_debt"},
                    set(diagnostic),
                )

    def _assert_no_float(self, value: object) -> None:
        self.assertNotIsInstance(value, float)
        if isinstance(value, dict):
            for child in value.values():
                self._assert_no_float(child)
        elif isinstance(value, list):
            for child in value:
                self._assert_no_float(child)

    def test_replayer_has_no_e001_runtime_imports(self) -> None:
        package = ROOT / "src" / "superloop_e002"
        for path in package.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports.append(node.module)
            self.assertFalse(
                any(name.startswith("superloop_e001") for name in imports),
                f"forbidden runtime import in {path}",
            )

    def test_full_matrix_reconstructs_without_invalid_runs(self) -> None:
        aggregate = replay_archive(ARCHIVE)
        self.assertEqual(72, aggregate["run_count"])
        self.assertEqual([], aggregate["invalid_run_ids"])
        self.assertEqual(
            "offline_supported_shadow_not_evaluated",
            aggregate["hypotheses"]["H1_noninterference"],
        )
        self.assertEqual("supported", aggregate["hypotheses"]["H2_coherent_reconstruction"])
        self.assertEqual("supported", aggregate["hypotheses"]["H3_typed_diagnostic_separation"])


if __name__ == "__main__":
    unittest.main()
