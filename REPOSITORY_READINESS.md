# Repository Readiness

This checklist separates repository operations from architectural and ownership decisions. A checked item should be verifiable in GitHub or in the repository history.

## Research foundation

- [x] Independent project charter and Aurora boundary drafted
- [x] Governance and evidence classes drafted
- [x] CBF and pneumatic source papers preserved with provenance
- [x] Minimal interlock contract drafted
- [x] CBF–pneumatic bridge formalized at E1
- [x] Bounded-emergence operating note drafted
- [ ] Foundation and bridge pull requests reviewed and merged to `main`

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

- [ ] Select a license or deliberately retain default copyright
- [ ] Decide whether external contributions are accepted before the first proof of concept
- [ ] Select allowed merge methods and history policy
- [ ] Enable automatic deletion of merged branches if desired
- [ ] Enable private vulnerability reporting
- [ ] Add repository description and topics
- [ ] Decide whether GitHub Discussions should be enabled for exploratory conversation

## Recommended `main` protection after the first CI run

- [ ] Require pull requests
- [ ] Require the `Repository integrity` status check
- [ ] Block force pushes and branch deletion
- [ ] Require conversation resolution
- [ ] Keep administrator bypass available only for documented recovery

## Proof-of-concept entrance criteria

- [ ] E001 has a standalone experiment specification
- [ ] Success, falsification, fault, and equivalence criteria are frozen before implementation
- [ ] Runtime and simulation-language choice is recorded as an ADR
- [ ] Simulated time is separated from wall-clock measurements
- [ ] Deterministic seed and trace formats are defined
- [ ] Central scheduler, global barrier, and local-interlock baselines share equivalent workloads
- [ ] Raw results and emergent observations have designated repository locations

## Current critical path

1. Review and merge the foundation pull request.
2. Retarget and merge the bridge pull request onto `main`.
3. Merge repository-readiness scaffolding.
4. Record the licensing and contribution-policy decisions.
5. Formalize E001 and choose the minimal simulator stack through an ADR.

