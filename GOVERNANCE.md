# Research Governance

## 1. Authority and scope

This repository governs Superloop Workshop only. It does not alter the status of any concept or artifact in Aurora, ORIONCORE, or another project.

## 2. Evidence classes

| Class | Meaning |
| --- | --- |
| E0 — Intuition | Conceptual reasoning without executable or empirical support |
| E1 — Formal sketch | Variables, rules, and expected properties are explicit |
| E2 — Reproducible prototype | A fixed environment reproduces declared behavior |
| E3 — Comparative evidence | The design is tested against relevant baselines |
| E4 — Adversarial evidence | Faults, delays, partitions, malformed inputs, and hostile topology are tested |
| E5 — Independent replication | A separate implementation or evaluator reproduces the result |

## 3. Promotion requirements

A concept may not become **Candidate** without E3 evidence. It may not become **Adopted** without E4 evidence, an explicit limitations section, and review of the relevant safety invariants.

## 4. Change discipline

Architecturally meaningful changes should include:

- the concept identifiers affected;
- the claim being changed;
- the evidence supporting the change;
- newly introduced failure modes;
- backward-compatibility or migration consequences;
- whether the change affects a hard invariant.

## 5. Hard boundaries

- Learned or adaptive parameters may not override identity, provenance, authorization, capacity, or prohibited-state rules.
- A stable state may not be called correct without a specification-appropriate validator.
- A bridge document may connect concepts but may not erase their separate provenance.
- Archived prototypes remain archived unless promoted through this repository's own evidence process.
- Negative results, abandoned hypotheses, and failed experiments must remain traceable.

## 6. Repository workflow

- Use focused branches for foundational or architectural changes.
- Prefer reviewable pull requests over direct changes to `main`.
- Record research hypotheses before running experiments.
- Store raw results separately from interpretation.
- Never rewrite an unsuccessful result to make a later model appear inevitable.

## 7. Licensing boundary

No open-source license is currently granted. A future licensing decision must consider the desired balance among public research, collaboration, defensive publication, and preservation of originator rights.

