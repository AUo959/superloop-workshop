# E002 Observation O001 — Scalar Flow Projection Asymmetry

**Artifact class:** Emergent observation
**Version:** v0.1
**Date:** 2026-07-14
**Status:** Preserved — requires a new experiment to extend
**Source experiment:** `SW.EXPERIMENT.E002`

## Observation

The fixed scalar candidate-flow law did not preserve the diagnostic value of the typed field state.

For wait or credit denial, `1 - F*` produced pooled ROC-AUC 0.368152, substantially below receiver congestion at 0.772791. For transfer commit, `F*` improved on the weak vacancy-only baseline in the pooled aggregate but remained near chance at 0.509871 and reached the required 0.70 AUC in no scenario. For healthy-loop stall, the pneumatic and baseline scores were exactly equal.

## Architectural significance

The result suggests that the field's useful structure is not a single congestion gradient. Transfers depend on distinctions the CBF contract treats as constitutional: readiness, receiver capacity, fault isolation, semantic validity, freshness, provenance, and reciprocal obligation state.

Multiplication into one scalar creates two characteristic losses:

1. A zero positive gradient suppresses candidate flow even when an equal-occupancy transfer is valid.
2. A capacity or fault barrier can dominate a transition for different reasons that should not become numerically interchangeable.

The observability layer remained coherent precisely because it kept those causes typed. The scalar projection became weak when it collapsed them.

## Relationship to E001 O001

E001 O001 found a sharp zero-vacancy liveness boundary for strictly local receiver-issued credit. E002 O001 adds a complementary finding: occupancy gradient alone cannot explain or predict the constitutional transition surface on either side of that boundary.

Together, the observations favor a vector or topological account of field state over an automatic scalar pressure law. They do not authorize cyclic exchange, global visibility, or a bypass.

## Governance boundary

This observation cannot be used to tune E002 after inspection. Any alternative vector, graph, phase, or topological projection requires a newly frozen experiment with declared targets and baselines. No causal scheduler follows from this observation.

## Evidence

- [E002 Stage B report](../results/reports/E002__STAGE_B_RESULTS__v0.1__2026-07-14.md)
- [Aggregate analysis](../results/summary/AGGREGATE_ANALYSIS__E002__a9923615.json)
- [E001 Observation O001](../../E001/observations/E001__OBSERVATION__FULL_RING_CIRCULATION_ASYMMETRY__v0.1__2026-07-14.md)
