# Architecture Decision Records

Decision records explain consequential choices without pretending that the current choice is permanent or inevitable.

## When to create a decision record

Create an ADR when choosing or changing:

- the proof-of-concept language or simulation runtime;
- the canonical state, event, or trace representation;
- a constitutive pressure or flow model;
- a hard invariant or validation boundary;
- a baseline, metric, or experimental comparison policy;
- a dependency with architectural consequences; or
- a repository policy that affects evidence or reproducibility.

## Naming

Use `ADR__NNNN__SHORT_DECISION_NAME__YYYY-MM-DD.md` with a stable sequence number.

Copy [the ADR template](ADR_TEMPLATE.md), fill every section, and link superseding decisions in both directions.

## Status values

- **Proposed** — open for focused review.
- **Accepted** — current project decision.
- **Trial** — accepted for a bounded experiment only.
- **Superseded** — replaced by a named later decision.
- **Rejected** — considered but deliberately not adopted.

## Current decisions

- [ADR 0001 — Python standard library for E001](ADR__0001__PYTHON_STANDARD_LIBRARY_FOR_E001__2026-07-13.md) — **Trial**
