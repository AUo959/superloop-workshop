# Validation Tests

Tests will be organized around architectural properties rather than implementation convenience.

## Required property families

- **Boundedness** — declared capacities are never exceeded.
- **Safety** — prohibited transitions remain unreachable.
- **Liveness** — admissible work progresses, degrades safely, or terminates accountably.
- **Idempotence** — replayed proposals do not duplicate state or authority.
- **Freshness** — expired feedback cannot authorize progress.
- **Fault containment** — local failure remains within a measurable radius.
- **Fairness** — persistent low-pressure work is not starved indefinitely.
- **Auditability** — every promoted state has a reconstructable causal path.
- **Self-stabilization** — supported transient faults return to a legitimate state.

Every implementation test should identify the concept invariant it protects.

E001 tests must map explicitly to the ten hard invariants in the [E001 specification](../experiments/E001/EXPERIMENT__E001__THREE_RING_BOUNDED_FLOW__v0.1__2026-07-13.md).

Run the Stage A suite with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -p "test_*.py" -v
```
