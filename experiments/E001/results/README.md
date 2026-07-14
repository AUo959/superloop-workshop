# E001 Results

This directory preserves reproducible evidence from the frozen E001 matrix.

## Layout

- `raw/` — canonical JSON Lines transition traces
- `summary/` — one machine-readable JSON summary per run
- `reports/` — aggregate comparisons and interpretation

Each result set must identify the experiment-specification version, source commit, configuration digest, workload digest, seed, invocation, Python version, and all failed or invalid runs.

Generated evidence must not be edited by hand. Corrections require a new run identifier and preserved supersession note.

## Canonical Stage A evidence

The first canonical matrix was generated from source commit `81e7f859f71425bdba7603a61566f9fb47c116f9` by [GitHub Actions run 29305465071](https://github.com/AUo959/superloop-workshop/actions/runs/29305465071) using CPython 3.13.14.

- [Compressed raw evidence](raw/E001__CANONICAL_EVIDENCE__81e7f859f71425bdba7603a61566f9fb47c116f9.tar.gz)
- [Archive checksum](raw/E001__CANONICAL_EVIDENCE__81e7f859f71425bdba7603a61566f9fb47c116f9.tar.gz.sha256)
- [Per-run summaries](summary/)
- [Matrix manifest](summary/MATRIX_MANIFEST__E001__81e7f859.json)
- [Provenance record](summary/PROVENANCE__E001__81e7f859.json)
- [Stage A report](reports/E001__STAGE_A_RESULTS__v0.1__2026-07-14.md)

The archive SHA-256 is `584cc15bfeb3cc74dec9d9069cde26e1abaa6f1350c0aa12ae10a9784bd1663b`.
