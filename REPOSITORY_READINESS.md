# Repository Readiness

This checklist separates repository operations from architectural and ownership decisions. A checked item should be verifiable in GitHub or in the repository history.

## Research foundation

- [x] Independent project charter and Aurora boundary drafted
- [x] Governance and evidence classes drafted
- [x] CBF and pneumatic source papers preserved with provenance
- [x] Minimal interlock contract drafted
- [x] CBF–pneumatic bridge formalized at E1
- [x] Bounded-emergence operating note drafted
- [x] Foundation and bridge pull requests reviewed and merged to `main`

## Contribution and evidence workflow

- [x] Pull-request research template
- [x] Experiment-proposal issue form
- [x] Emergent-observation issue form
- [x] Defect-report issue form
- [x] Architecture decision record template
- [x] CODEOWNERS baseline
- [x] Stack-neutral editor, line-ending, and ignore rules
- [x] Repository-integrity workflow

## Owner decisions before public collaboration

- [x] Deliberately retain default copyright during the initial proof of concept
- [x] Keep implementation contributions maintainer-led through E001
- [x] Use squash merges for focused project history
- [x] Enable automatic deletion of merged branches
- [x] Enable private vulnerability reporting
- [x] Add repository description and topics
- [x] Defer GitHub Discussions until the first proof of concept is reproducible

## Recommended `main` protection after the first CI run

- [x] Require pull requests
- [x] Require the `Repository integrity` status check
- [x] Block force pushes and branch deletion
- [x] Require conversation resolution
- [x] Keep no standing bypass actor in the active `main` ruleset

## Proof-of-concept entrance criteria

- [x] E001 has a standalone experiment specification
- [x] Success, falsification, fault, and equivalence criteria are frozen before implementation
- [x] Runtime and simulation-language choice is recorded as an ADR
- [x] Simulated time is separated from wall-clock measurements
- [x] Deterministic seed and trace formats are defined
- [x] Central scheduler, global barrier, and local-interlock baselines share equivalent workloads
- [x] Raw results and emergent observations have designated repository locations

## Current critical path

1. Implement the E002 offline trace replayer without simulator imports.
2. Verify exact state reconstruction and byte-identical telemetry repetition.
3. Add optional shadow mode and prove Stage A trace noninterference.
4. Replay all 72 E001 runs and evaluate the frozen diagnostic thresholds.
5. Classify each pneumatic projection as retain, narrow, revise, or reject.

## E001 Stage A completion

- [x] Discrete three-ring observation chamber implemented
- [x] Tests mapped to the E001 invariant families
- [x] Canonical 72-run matrix repeated under Python 3.13
- [x] Raw evidence, summaries, provenance, and checksum preserved
- [x] Directed results and emergent observations separated
- [x] Exit decision recorded: proceed with noncausal Stage B instrumentation

## E002 Stage B entrance criteria

- [x] E002 has a standalone experiment specification
- [x] Source E001 evidence and archive digest are frozen
- [x] Offline replay and exact rational representation are recorded as an ADR
- [x] Sampling order and no-lookahead rule are explicit
- [x] Pneumatic variables are prohibited from changing Stage A transitions
- [x] Fixed diagnostic baselines and thresholds are declared before implementation
- [x] Retain, narrow, revise, and reject outcomes are defined
