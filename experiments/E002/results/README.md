# E002 Results

This directory will preserve noncausal telemetry derived from the frozen E001 evidence set.

## Layout

- `raw/` — canonical JSON Lines telemetry, stored separately from E001 traces
- `summary/` — one machine-readable instrumentation summary per source run
- `reports/` — aggregate validity, diagnostic, and interpretation reports

Every result set must identify the E002 specification and configuration digests, implementation commit, source E001 run and trace digest, invocation, runtime, and every invalid or omitted run.

Generated telemetry may not overwrite E001 evidence. Corrections require a new result identifier and preserved supersession record.

No E002 evidence has been produced yet.
