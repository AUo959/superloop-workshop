# Contributing to Superloop Workshop

Superloop Workshop welcomes rigorous speculation, formalization, simulation, critique, and falsification.

## Before proposing a change

Identify:

1. the concept or experiment affected;
2. the claim being introduced or changed;
3. its current evidence class;
4. the result that would falsify it;
5. any new safety, liveness, or governance risk.

## Research contributions

Research notes should distinguish:

- observation;
- inference;
- hypothesis;
- implementation decision;
- measured result;
- unresolved uncertainty.

## Code contributions

Reference implementations should be deterministic by default, use explicit seeds where randomness is necessary, and emit machine-readable traces sufficient to reconstruct each state transition.

Tests should cover success, overload, stale feedback, malformed state, circular wait, partition, and recovery—not only the happy path.

## Architectural independence

Do not import Aurora modules, names, or canon implicitly. If prior work informs a contribution, identify the relationship and explain why the mechanism belongs independently in Superloop Workshop.

