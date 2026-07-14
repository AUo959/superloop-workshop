"""Generate a reproducible E001 evidence set from the frozen Stage A matrix."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
from typing import Any

from superloop_e001.model import canonical_json, digest
from superloop_e001.simulator import RunResult, matrix_manifest, run_matrix


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CONFIGURATION_PATH = (
    REPOSITORY_ROOT
    / "experiments"
    / "E001"
    / "config"
    / "CANONICAL_MATRIX__E001__v0.1__2026-07-13.json"
)
SPECIFICATION_PATH = (
    REPOSITORY_ROOT
    / "experiments"
    / "E001"
    / "EXPERIMENT__E001__THREE_RING_BOUNDED_FLOW__v0.1__2026-07-13.md"
)


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _determinism_mismatches(
    first: list[RunResult],
    second: list[RunResult],
) -> list[str]:
    mismatches: list[str] = []
    second_by_run = {result.summary["run_id"]: result for result in second}
    for result in first:
        run_id = result.summary["run_id"]
        repeated = second_by_run.get(run_id)
        if repeated is None:
            mismatches.append(f"{run_id}:missing_repeat")
            continue
        if result.trace_jsonl != repeated.trace_jsonl:
            mismatches.append(f"{run_id}:trace")
        if result.summary != repeated.summary:
            mismatches.append(f"{run_id}:summary")
    unexpected = sorted(set(second_by_run) - {result.summary["run_id"] for result in first})
    mismatches.extend(f"{run_id}:unexpected_repeat" for run_id in unexpected)
    return mismatches


def generate(output: Path, source_commit: str) -> dict[str, Any]:
    """Run, repeat, validate, and write the frozen E001 matrix."""

    if output.exists() and any(output.iterdir()):
        raise ValueError(f"output directory is not empty: {output}")
    raw_dir = output / "raw"
    summary_dir = output / "summary"
    inputs_dir = output / "inputs"
    raw_dir.mkdir(parents=True, exist_ok=True)
    summary_dir.mkdir(parents=True, exist_ok=True)
    inputs_dir.mkdir(parents=True, exist_ok=True)

    first = run_matrix()
    second = run_matrix()
    mismatches = _determinism_mismatches(first, second)
    manifest = matrix_manifest(first)
    manifest["determinism_mismatches"] = mismatches
    manifest["source_commit"] = source_commit

    for result in first:
        run_id = result.summary["run_id"]
        (raw_dir / f"{run_id}.jsonl").write_text(
            result.trace_jsonl,
            encoding="utf-8",
        )
        _write_json(summary_dir / f"{run_id}.json", result.summary)

    configuration_bytes = CONFIGURATION_PATH.read_bytes()
    specification_bytes = SPECIFICATION_PATH.read_bytes()
    (inputs_dir / CONFIGURATION_PATH.name).write_bytes(configuration_bytes)
    _write_json(output / "matrix_manifest.json", manifest)

    provenance = {
        "schema_version": "e001.evidence-provenance.v1",
        "experiment": "SW.EXPERIMENT.E001",
        "source_commit": source_commit,
        "specification": {
            "path": str(SPECIFICATION_PATH.relative_to(REPOSITORY_ROOT)),
            "sha256": _sha256_bytes(specification_bytes),
        },
        "configuration": {
            "path": str(CONFIGURATION_PATH.relative_to(REPOSITORY_ROOT)),
            "sha256": _sha256_bytes(configuration_bytes),
        },
        "invocation": (
            "PYTHONPATH=src python tools/generate_e001_evidence.py "
            f"--output build/e001-canonical --source-commit {source_commit}"
        ),
        "runtime": {
            "implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
        },
        "validation": {
            "determinism_mismatches": mismatches,
            "invalid_run_ids": manifest["invalid_run_ids"],
            "run_count": manifest["run_count"],
            "workload_equivalence_mismatches": manifest[
                "workload_equivalence_mismatches"
            ],
        },
        "matrix_manifest_digest": digest(manifest),
    }
    _write_json(output / "provenance.json", provenance)

    if mismatches:
        raise RuntimeError(f"determinism mismatches: {mismatches}")
    if manifest["invalid_run_ids"]:
        raise RuntimeError(f"invalid runs: {manifest['invalid_run_ids']}")
    if manifest["workload_equivalence_mismatches"]:
        raise RuntimeError(
            "workload equivalence mismatches: "
            f"{manifest['workload_equivalence_mismatches']}"
        )
    return provenance


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    provenance = generate(args.output, args.source_commit)
    print(canonical_json(provenance))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
