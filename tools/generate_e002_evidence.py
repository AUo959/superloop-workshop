"""Generate deterministic E002 telemetry and analysis from frozen E001 evidence."""

from __future__ import annotations

import argparse
import gzip
import json
import platform
import tarfile
from pathlib import Path

from superloop_e002.model import canonical_json, raw_digest
from superloop_e002.replayer import replay_archive


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARCHIVE = (
    REPOSITORY_ROOT
    / "experiments"
    / "E001"
    / "results"
    / "raw"
    / "E001__CANONICAL_EVIDENCE__81e7f859f71425bdba7603a61566f9fb47c116f9.tar.gz"
)


def _write_json(path: Path, value: dict[str, object]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _deterministic_archive(source: Path, destination: Path) -> None:
    with destination.open("wb") as raw_output:
        with gzip.GzipFile(fileobj=raw_output, mode="wb", mtime=0, filename="") as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as archive:
                for path in sorted(source.rglob("*")):
                    if not path.is_file():
                        continue
                    info = archive.gettarinfo(str(path), arcname=str(path.relative_to(source)))
                    info.mtime = 0
                    info.uid = 0
                    info.gid = 0
                    info.uname = ""
                    info.gname = ""
                    with path.open("rb") as handle:
                        archive.addfile(info, handle)


def generate(output: Path, archive_path: Path, source_commit: str) -> dict[str, object]:
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"output directory is not empty: {output}")
    raw_directory = output / "raw"
    summary_directory = output / "summary"
    output.mkdir(parents=True, exist_ok=True)
    aggregate = replay_archive(archive_path, raw_directory, summary_directory)
    repeated = replay_archive(archive_path)
    determinism_mismatches: list[str] = []
    if aggregate["aggregate_digest"] != repeated["aggregate_digest"]:
        determinism_mismatches.append("aggregate_analysis")
    if aggregate["run_summary_digests"] != repeated["run_summary_digests"]:
        determinism_mismatches.append("run_summaries_or_telemetry")
    _write_json(output / "aggregate_analysis.json", aggregate)
    provenance: dict[str, object] = {
        "schema_version": "e002.evidence-provenance.v1",
        "experiment": "SW.EXPERIMENT.E002",
        "source_commit": source_commit,
        "source_e001_archive_sha256": raw_digest(archive_path.read_bytes()),
        "invocation": (
            "PYTHONPATH=src python tools/generate_e002_evidence.py "
            f"--output {output} --source-commit {source_commit}"
        ),
        "runtime": {
            "implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
        },
        "validation": {
            "run_count": aggregate["run_count"],
            "telemetry_record_count": aggregate["telemetry_record_count"],
            "invalid_run_ids": aggregate["invalid_run_ids"],
            "determinism_mismatches": determinism_mismatches,
        },
        "aggregate_digest": aggregate["aggregate_digest"],
    }
    _write_json(output / "provenance.json", provenance)
    archive_output = output.parent / f"{output.name}.tar.gz"
    _deterministic_archive(output, archive_output)
    (archive_output.with_suffix(archive_output.suffix + ".sha256")).write_text(
        f"{raw_digest(archive_output.read_bytes())}  {archive_output.name}\n",
        encoding="utf-8",
    )
    if aggregate["invalid_run_ids"]:
        raise RuntimeError(f"invalid E002 runs: {aggregate['invalid_run_ids']}")
    if determinism_mismatches:
        raise RuntimeError(f"E002 determinism mismatches: {determinism_mismatches}")
    return provenance


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--source-commit", required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    provenance = generate(args.output, args.archive, args.source_commit)
    print(canonical_json(provenance))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
