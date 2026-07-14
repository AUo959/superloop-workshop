# E002 Results

This directory will preserve noncausal telemetry derived from the frozen E001 evidence set.

## Layout

- `raw/` — canonical JSON Lines telemetry, stored separately from E001 traces
- `summary/` — one machine-readable instrumentation summary per source run
- `reports/` — aggregate validity, diagnostic, and interpretation reports

Every result set must identify the E002 specification and configuration digests, implementation commit, source E001 run and trace digest, invocation, runtime, and every invalid or omitted run.

Generated telemetry may not overwrite E001 evidence. Corrections require a new result identifier and preserved supersession record.

The canonical generator is `tools/generate_e002_evidence.py`; the protected runner is `.github/workflows/e002-canonical-evidence.yml`. The generator repeats the full replay and rejects run-summary, telemetry-digest, or aggregate-analysis drift before packaging evidence.

## Canonical result

- [Stage B directed report](reports/E002__STAGE_B_RESULTS__v0.1__2026-07-14.md) — **Completed / Narrow**
- [Aggregate analysis](summary/AGGREGATE_ANALYSIS__E002__a9923615.json)
- [Provenance](summary/PROVENANCE__E002__a9923615.json)
- [Compressed evidence](raw/E002__CANONICAL_EVIDENCE__a9923615c09a7cd1afc452c16e505d70b98c0568.tar.gz)
- [Archive checksum](raw/E002__CANONICAL_EVIDENCE__a9923615c09a7cd1afc452c16e505d70b98c0568.tar.gz.sha256)

The evidence completed all 72 source replays under Python 3.13 with zero invalid runs or determinism mismatches. H2 and H3 were supported, offline H1 was supported while optional shadow parity remained unevaluated, and H4 was not supported. The tested scalar law is not authorized for causal use.
