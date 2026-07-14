"""Command-line interface for E001 Stage A."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .simulator import matrix_manifest, run_matrix, run_simulation, write_result
from .workloads import CONFIGURATIONS, SCENARIOS, SEEDS


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the deterministic E001 observation chamber.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run one canonical configuration.")
    run_parser.add_argument("--configuration", choices=CONFIGURATIONS, required=True)
    run_parser.add_argument("--scenario", choices=SCENARIOS, required=True)
    run_parser.add_argument("--seed", choices=SEEDS, type=int, required=True)
    run_parser.add_argument("--output", type=Path)
    run_parser.add_argument("--print-summary", action="store_true")

    matrix_parser = subparsers.add_parser("matrix", help="Run all 72 canonical configurations.")
    matrix_parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "run":
        result = run_simulation(args.configuration, args.scenario, args.seed)
        if args.output:
            write_result(result, args.output)
        if args.print_summary or not args.output:
            print(json.dumps(result.summary, ensure_ascii=False, indent=2, sort_keys=True))
        return int(result.summary["invariant_violation_count"] > 0)

    results = run_matrix()
    for result in results:
        write_result(result, args.output)
    manifest = matrix_manifest(results)
    (args.output / "matrix_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return int(bool(manifest["invalid_run_ids"] or manifest["workload_equivalence_mismatches"]))


if __name__ == "__main__":
    raise SystemExit(main())

