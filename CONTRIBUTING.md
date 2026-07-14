# Contributing to Superloop Workshop

Superloop Workshop welcomes rigorous speculation, formalization, simulation, critique, and falsification.

## Before proposing a change

Identify:

1. the concept or experiment affected;
2. the claim being introduced or changed;
3. its current evidence class;
4. the result that would falsify it;
5. any new safety, liveness, or governance risk.

Use the repository issue forms to propose experiments, record emergent observations, or report defects. Consequential implementation and architecture choices should receive an [Architecture Decision Record](docs/decisions/README.md).

## Research contributions

Research notes should distinguish:

- observation;
- inference;
- hypothesis;
- implementation decision;
- measured result;
- unresolved uncertainty.

Every experiment should preserve two distinct outputs:

1. directed evidence about its declared hypothesis; and
2. emergent observations that were not part of the intended result.

Emergent behavior remains a Seed until it is reproduced, formalized, and tested. See [Bounded Emergence](docs/research/BOUNDED_EMERGENCE__OPERATING_NOTE__v0.1__2026-07-13.md).

## Code contributions

Reference implementations should be deterministic by default, use explicit seeds where randomness is necessary, and emit machine-readable traces sufficient to reconstruct each state transition.

Tests should cover success, overload, stale feedback, malformed state, circular wait, partition, and recovery—not only the happy path.

## Architectural independence

Do not import Aurora modules, names, or canon implicitly. If prior work informs a contribution, identify the relationship and explain why the mechanism belongs independently in Superloop Workshop.

## Pull-request workflow

- Use a focused branch and a reviewable pull request.
- Complete the research identity, falsifier, provenance, safety, and validation sections of the pull-request template.
- Keep generated output and raw evidence separate from source code.
- Do not rewrite negative results; supersede interpretations with traceable follow-up work.
- Do not include credentials, private datasets, or external canonical artifacts.

