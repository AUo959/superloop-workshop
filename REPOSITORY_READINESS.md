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

1. Preserve E002's Narrow result and do not tune the frozen scalar law.
2. Decide whether a new noncausal vector/topological experiment has a question distinct enough to justify E003.
3. Freeze any E003 targets and baselines before implementation.
4. Defer optional shadow mode unless a noncausal projection first demonstrates value.
5. Preserve any causal Stage C proposal as a separate, newly frozen experiment.

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

## E002 Stage B implementation

- [x] Offline archive reader verifies the frozen E001 archive and embedded digests
- [x] Replayer has no E001 simulator or workload imports
- [x] Tick-boundary state reconstruction covers all 72 source runs
- [x] Exact-rational loop and interlock telemetry is deterministic
- [x] Typed capacity, fault, semantic, stale-authority, and reciprocal-debt channels are separate
- [x] Fixed T1–T3 analysis and exact ROC-AUC calculation are implemented
- [x] Protected Python 3.13 evidence workflow is defined
- [x] Canonical Python 3.13 evidence archive verified and promoted
- [x] Directed result and Narrow outcome classification recorded
- [x] Scalar projection asymmetry preserved as an emergent observation
- [x] Causal Stage C progression declined for the tested law
