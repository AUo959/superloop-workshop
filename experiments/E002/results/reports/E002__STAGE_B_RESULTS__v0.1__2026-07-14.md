# E002 Stage B Results — Noncausal Pneumatic Instrumentation

**Artifact class:** Observational experiment report
**Version:** v0.1
**Date:** 2026-07-14
**Status:** Completed — Narrow
**Evidence class:** E4-scoped negative and reconstructive evidence within the E001 model
**Experiment:** `SW.EXPERIMENT.E002`
**Exit decision:** **Do not proceed** to causal Stage C with the tested scalar flow law

## 1. Result in one sentence

The pneumatic layer reconstructed all 72 E001 runs exactly and preserved the required diagnostic distinctions, but its fixed scalar candidate-flow projection failed the predeclared scenario-general usefulness threshold and therefore remains descriptive rather than constitutive.

This result is evidence about a read-only projection of the frozen three-loop traces. It is not evidence of physical thermodynamics, pneumatic equivalence, calibrated energy, neural computation, or production-scale behavior.

## 2. Canonical evidence identity

| Property | Value |
| --- | --- |
| Implementation commit | [`a9923615c09a7cd1afc452c16e505d70b98c0568`](https://github.com/AUo959/superloop-workshop/commit/a9923615c09a7cd1afc452c16e505d70b98c0568) |
| Source E001 commit | `81e7f859f71425bdba7603a61566f9fb47c116f9` |
| Runtime | CPython 3.13.11, standard library only |
| Execution route | Manual canonical invocation after local and fetched `main` tree equality was verified |
| E002 specification SHA-256 | `badb4844084fc14adf20935868941a95feebe724e366baa3dc4afdaf297b9821` |
| Instrumentation contract SHA-256 | `ab34a99d031630a00ce28b3785330a764eab8f1a7ff5eca07cb4afc8ffb4feae` |
| Source E001 archive SHA-256 | `584cc15bfeb3cc74dec9d9069cde26e1abaa6f1350c0aa12ae10a9784bd1663b` |
| E002 aggregate digest | `41d35fba334b4f23c773d16f78b6e7fe6939b4d43ca69f7b8827ea897af82898` |
| E002 archive SHA-256 | `df090ed18647b3e793ecb8dffef5bbf1af3a7f679b4ffffb2d3c00103bfd5d08` |
| Runs | 72 |
| Telemetry records | 207,360 |
| Reconstruction accounting checks | 48,600 |
| Determinism mismatches | 0 |
| Invalid runs | 0 |

The Python 3.13 aggregate digest is byte-identical to the preceding Python 3.12 dry-run aggregate digest. The repository preserves the [compressed canonical evidence](../raw/E002__CANONICAL_EVIDENCE__a9923615c09a7cd1afc452c16e505d70b98c0568.tar.gz), its [checksum](../raw/E002__CANONICAL_EVIDENCE__a9923615c09a7cd1afc452c16e505d70b98c0568.tar.gz.sha256), all [run summaries](../summary/), the [aggregate analysis](../summary/AGGREGATE_ANALYSIS__E002__a9923615.json), and the [provenance record](../summary/PROVENANCE__E002__a9923615.json).

## 3. Validity gate

The offline E002 implementation passes its hard validity gate:

- the frozen E001 archive, manifest, trace digests, summary self-digests, and event sequences verified before replay;
- all 72 source runs reconstructed without E001 simulator or workload imports;
- reconstructed post-tick occupancy-time matched every E001 run summary exactly;
- every canonical rational was reduced and no canonical float, infinity, or `NaN` was emitted;
- pre-tick lineage contained no same-tick or future event identifier;
- capacity blockage, fault state, semantic rejection, stale authority, and reciprocal debt remained separate typed channels;
- all ten instrumentation invariants passed for every run; and
- repeated instrumentation produced identical telemetry, run-summary, and aggregate digests.

The generator emitted no E001 transition and did not modify the source evidence.

## 4. Hypothesis disposition

| Hypothesis | Disposition | Evidence |
| --- | --- | --- |
| H1 — Exact noninterference | Offline clause supported; optional shadow clause not evaluated | The replayer is a separate read-only process with no E001 runtime imports, and every source digest remained unchanged. No in-process shadow observer was added. |
| H2 — Coherent reconstruction | Supported | All 72 runs, 207,360 records, 48,600 declared occupancy checks, work ledgers, modes, readiness states, and occupancy-time identities reconstructed without an invalid run. |
| H3 — Typed diagnostic separation | Supported | Capacity, fault, semantic, stale-authority, and debt states remained separate; unavailable trust and uncertainty stayed `not_observed`. |
| H4 — Diagnostic usefulness | Not supported | No target met both the six-of-eight scenario AUC threshold and pooled lift threshold. |

H1 is deliberately not overstated. Offline noninterference is demonstrated by construction and digest verification; shadow-mode parity remains unevaluated and is not needed to interpret the offline negative result.

## 5. Fixed diagnostic comparisons

Decimal AUC values below are noncanonical renderings of the preserved exact fractions.

| Target | Pneumatic pooled AUC | Scalar baseline AUC | Lift | Scenarios at AUC ≥ 0.70 | Threshold result |
| --- | ---: | ---: | ---: | ---: | --- |
| T1 — wait or credit denial | 0.368152 | 0.772791 | -0.404639 | 0 of 8 | Fail |
| T2 — transfer commit | 0.509871 | 0.429770 | +0.080101 | 0 of 8 | Fail |
| T3 — healthy-loop stall within five ticks | 0.989479 | 0.989479 | 0 | 3 of 8 | Fail |

### 5.1 T1 — Wait or credit denial

The tested score `1 - F*` was materially worse than receiver congestion. Five scenarios contained no positive T1 case, so their AUC was correctly undefined rather than coerced to zero. In the three discriminating scenarios, no pneumatic AUC reached 0.70.

The direction matters: multiplying eligibility, vacancy conductance, and positive congestion gradient suppresses the score in several states where waits are caused by full capacity or fault boundaries. The scalar does not compress those typed causes safely.

### 5.2 T2 — Transfer commit

Candidate flow exceeded the simple vacancy baseline in the pooled comparison by approximately 0.0801, but its pooled AUC remained only 0.5099 and no scenario reached the 0.70 threshold. The positive pooled lift is therefore not scenario-general evidence of useful transfer prediction.

The result rejects the temptation to select only the favorable pooled lift. The predeclared decision required both lift and scenario coverage.

### 5.3 T3 — Healthy-loop stall

The pneumatic score and raw congestion baseline were exactly identical. Both separated the three scenarios containing positive stall cases extremely well, but the pneumatic formulation added no information or compression beyond its declared scalar input. T3 is coherent but redundant.

## 6. What the negative result reveals

The failure is informative. A transfer in this model is not governed by a single occupancy gradient. It also depends on local readiness, capacity, fault mode, schema and provenance validity, lease freshness, and reciprocal obligation handling. Those dimensions were intentionally kept separate by the CBF constitution.

The tested `F* = eligibility × conductance × positive gradient` collapses that structure too aggressively. Equal-occupancy exchanges have zero gradient even when a transfer is valid, while zero receiver vacancy can represent a capacity boundary that should remain typed rather than absorbed into one pressure score.

This supports the original architectural caution: pneumatic language is most coherent here as a vector observability layer around constitutional interlocks, not as a replacement operating system or automatic scalar scheduler.

The projection asymmetry is preserved separately as [E002 Observation O001](../../observations/E002__OBSERVATION__SCALAR_FLOW_PROJECTION_ASYMMETRY__v0.1__2026-07-14.md).

## 7. Outcome classification

The overall E002 outcome is **Narrow**.

Retain as noncausal observability:

- exact congestion and vacancy;
- typed finite resistance and zero-vacancy blockage;
- separate pressure-vector channels;
- typed capacity, fault, semantic, stale-authority, and debt states;
- integer phase indices as descriptive activity labels;
- occupancy-time and zero-vacancy-cycle diagnostics; and
- the offline reconstruction and evidence pipeline.

Narrow or reject as demonstrated diagnostics:

- reject `1 - F*` for T1 denial prediction in this model;
- narrow `F*` to an explicitly experimental descriptor, not a transfer predictor;
- treat the T3 resistance score as a restatement of congestion, not independent pneumatic evidence;
- make no usefulness claim for phase or dissipation beyond deterministic description; and
- do not fit weights or alter the frozen formula after seeing this result.

## 8. Exit decision

**Do not proceed to causal Stage C with the tested scalar law.**

The evidence does not justify allowing `F*`, resistance, dissipation, or phase to authorize work or replace the minimal interlock contract. Optional shadow instrumentation is also deferred because it would prove parity for a projection that has not demonstrated sufficient diagnostic value.

A later experiment may test a fixed vector or topological diagnostic that preserves readiness, typed barriers, and zero-vacancy cycles without scalar collapse. That work must receive a new experiment identifier, frozen targets, and equivalent-work controls. It may not be described as a tuned rerun of E002.

## 9. Limitations

- The evidence inherits E001's three-loop, one-direction topology and deterministic workloads.
- The eight scenarios are adversarial within the model, not independent external replication.
- AUC is undefined in scenarios with only one target class; undefined values cannot support H4.
- T3's high AUC reflects the same congestion information in both compared scores.
- Phase and dissipation were recorded but did not receive separate calibrated targets.
- No continuous fluid dynamics, physical pressure, energy, hardware cost, wall-clock behavior, or learning was modeled.
- Shadow-mode noninterference was not evaluated.

## 10. Reproduction

After checking out the implementation commit, run:

```bash
PYTHONPATH=src python tools/generate_e002_evidence.py \
  --output build/e002-canonical \
  --source-commit a9923615c09a7cd1afc452c16e505d70b98c0568
```

Verify the preserved archive from `experiments/E002/results/raw/` with:

```bash
sha256sum --check \
  E002__CANONICAL_EVIDENCE__a9923615c09a7cd1afc452c16e505d70b98c0568.tar.gz.sha256
```
