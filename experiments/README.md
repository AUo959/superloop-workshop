# Experiments

Experiments convert Superloop claims into reproducible evidence. Each experiment should preserve its hypothesis, configuration, raw trace, analysis, and negative results.

## E001 — Three-Ring Bounded Flow

**Status:** [Specified — E1](E001/EXPERIMENT__E001__THREE_RING_BOUNDED_FLOW__v0.1__2026-07-13.md)

**Registry ID:** `SW.EXPERIMENT.E001`

### Question

Can three recurrent units coordinate work through local interlocks while maintaining bounded queues and recovering from a slow or failed neighbor?

### Configurations

1. Central scheduler
2. Global barrier
3. Local CBF interlocks with credits and backpressure

### Required scenarios

- balanced steady load;
- burst load;
- saturated receiver;
- slow neighbor;
- failed neighbor;
- circular wait;
- stale feedback;
- malformed or duplicated proposal.

### Required metrics

- maximum queue occupancy;
- throughput and latency;
- admitted, rejected, revised, and expired proposals;
- fairness and starvation time;
- recovery time;
- fault radius;
- provenance completeness;
- transition count and coordination overhead.

### Success condition

The CBF configuration remains bounded and live under the declared normal and degraded cases, or produces a clear negative result identifying which architectural assumption failed. The standalone specification freezes the comparison contract, run matrix, invariants, and evidence locations.
