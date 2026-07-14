# E002 Results

This directory will preserve noncausal telemetry derived from the frozen E001 evidence set.

## Layout

- `raw/` — canonical JSON Lines telemetry, stored separately from E001 traces
- `summary/` — one machine-readable instrumentation summary per source run
- `reports/` — aggregate validity, diagnostic, and interpretation reports

Every result set must identify the E002 specification and configuration digests, implementation commit, source E001 run and trace digest, invocation, runtime, and every invalid or omitted run.

Generated telemetry may not overwrite E001 evidence. Corrections require a new result identifier and preserved supersession record.

The canonical generator is `tools/generate_e002_evidence.py`; the protected runner is `.github/workflows/e002-canonical-evidence.yml`. The generator repeats the full replay and rejects run-summary, telemetry-digest, or aggregate-analysis drift before packaging evidence.

No E002 evidence has been promoted yet. Implementation availability is not an experiment result; interpretation begins only after a digest-linked runner artifact is verified.
