# Source Implementations

No permanent reference runtime has been adopted. [ADR 0001](../docs/decisions/ADR__0001__PYTHON_STANDARD_LIBRARY_FOR_E001__2026-07-13.md) selects Python 3.13 and the standard library as a reversible trial for E001 Stage A.

The first implementation should be a deterministic discrete-event simulator with:

- explicit CBL state machines;
- stateful interlocks;
- bounded queues and capacity credits;
- simulated rather than wall-clock time;
- machine-readable transition traces;
- seeded fault injection;
- interchangeable centralized, global-barrier, and local-interlock schedulers.

The implementation must conform to the [frozen E001 specification](../experiments/E001/EXPERIMENT__E001__THREE_RING_BOUNDED_FLOW__v0.1__2026-07-13.md). A later runtime may replace Python if it preserves canonical inputs, traces, and declared semantics.

## E001 Stage A

The dependency-free simulator lives in `src/superloop_e001/` and can run one configuration or the complete canonical matrix:

```bash
PYTHONPATH=src python -m superloop_e001 run \
  --configuration local_cbf \
  --scenario balanced \
  --seed 17 \
  --print-summary

PYTHONPATH=src python -m superloop_e001 matrix --output /tmp/e001-results
```

The matrix command writes generated evidence only to an explicit output directory. Canonical repository evidence should be promoted separately after review of the source commit and complete manifest.
