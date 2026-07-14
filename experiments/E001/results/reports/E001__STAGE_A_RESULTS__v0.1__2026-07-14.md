# E001 Stage A Results — Three-Ring Bounded Flow

**Artifact class:** Comparative experiment report  
**Version:** v0.1  
**Date:** 2026-07-14  
**Status:** Completed  
**Evidence class:** E4 within the declared E001 model  
**Experiment:** `SW.EXPERIMENT.E001`  
**Exit decision:** **Proceed** to noncausal Stage B instrumentation

## 1. Result in one sentence

The local CBF configuration preserved every hard invariant and contained a failed neighbor more locally than the global barrier, but it paid substantially higher coordination cost and could not circulate an exactly full ring without a free receiver slot.

This is evidence about the frozen three-loop simulator only. It is not evidence of physical thermodynamic equivalence, production-scale performance, or superiority to mature distributed systems.

## 2. Canonical evidence identity

| Property | Value |
| --- | --- |
| Source commit | [`81e7f859f71425bdba7603a61566f9fb47c116f9`](https://github.com/AUo959/superloop-workshop/commit/81e7f859f71425bdba7603a61566f9fb47c116f9) |
| GitHub Actions run | [`29305465071`](https://github.com/AUo959/superloop-workshop/actions/runs/29305465071) |
| Runtime | CPython 3.13.14 |
| Specification SHA-256 | `b3552734244244699114dee7710b030c9ec584262c13bef97961008b375faa60` |
| Configuration SHA-256 | `c95b449048b620d2a6a866ff43db675b085951086710828fe03391f268012d11` |
| Matrix-manifest digest | `4ae44e0f3e0029f9f124b2f30ee28f5d83e476cd5135f1f5233930424ac3fe42` |
| Canonical archive SHA-256 | `584cc15bfeb3cc74dec9d9069cde26e1abaa6f1350c0aa12ae10a9784bd1663b` |
| Runs | 72 |
| Repeated executions | 72 |
| Determinism mismatches | 0 |
| Invalid runs | 0 |
| Workload-equivalence mismatches | 0 |

The repository preserves the [compressed canonical evidence](../raw/E001__CANONICAL_EVIDENCE__81e7f859f71425bdba7603a61566f9fb47c116f9.tar.gz), its [checksum](../raw/E001__CANONICAL_EVIDENCE__81e7f859f71425bdba7603a61566f9fb47c116f9.tar.gz.sha256), all [run summaries](../summary/), the [matrix manifest](../summary/MATRIX_MANIFEST__E001__81e7f859.json), and the [provenance record](../summary/PROVENANCE__E001__81e7f859.json).

## 3. Validity gate

Stage A passes its predeclared validity gate:

- all 72 runs produced byte-identical traces and summaries when repeated;
- all configurations consumed equivalent canonical workloads;
- maximum recorded occupancy was 8, equal to declared capacity;
- no run ended with active work or unresolved obligations;
- no run authorized stale feedback or duplicated promotion;
- provenance completeness was 100% for every promoted item; and
- every hard-invariant count was zero.

No failed or unfavorable run was removed from the matrix.

## 4. Hypothesis disposition

| Hypothesis | Disposition | Evidence |
| --- | --- | --- |
| H1 — Bounded admission | Supported | Occupancy never exceeded 8; all ledgers balanced; all work reached an accountable state. |
| H2 — Local fault containment | Supported for failed-neighbor S5; not discriminated by slow-neighbor S4 | In S5, local CBF had fault radius 1 and 15 healthy-progress ticks versus radius 2 and 10 ticks for the global barrier across all seeds. All configurations tied in S4. |
| H3 — Reciprocal accountability | Supported | Every stale replay was rejected, malformed and duplicate offers were terminally classified, duplicate promotion remained zero, and provenance remained complete. |
| H4 — Coordination tradeoff | Supported with material cost and a saturation boundary | Obligations remained bounded and waits terminated accountably, but local CBF used more coordination events and expired the exactly full circular workload. |

## 5. Directed comparisons

### 5.1 Failed neighbor

Values separated by `/` correspond to seeds 17, 29, and 43.

| Configuration | Completed | Healthy-progress ticks | Fault radius | Maximum wait | Coordination events |
| --- | ---: | ---: | ---: | ---: | ---: |
| Central | 35 / 35 / 35 | 15 / 15 / 15 | 1 / 1 / 1 | 37 / 37 / 37 | 179 / 179 / 179 |
| Global barrier | 36 / 36 / 36 | 10 / 10 / 10 | 2 / 2 / 2 | 40 / 40 / 40 | 219 / 219 / 219 |
| Local CBF | 36 / 36 / 35 | 15 / 15 / 15 | 1 / 1 / 1 | 37 / 37 / 37 | 411 / 411 / 397 |

Local CBF matches the central baseline's containment measurements and improves on the global barrier's fault radius and healthy progress. It does not outperform the central baseline, and its coordination cost is more than twice the central count in this scenario.

### 5.2 Normal and burst load

All configurations completed all offered work with equal simulated throughput under balanced and burst load. Local CBF used 320 coordination events instead of 160 for balanced load and 512 instead of 256 for burst load. The additional protocol work produced no throughput advantage in these cases.

### 5.3 Slow neighbor

All configurations completed 40 items with 33 healthy-progress ticks, fault radius 0, recovery time 0, and maximum wait 0 for every seed. S4 is therefore non-discriminating at the frozen load and service parameters. Local CBF still used 320 coordination events versus 160 for each baseline.

### 5.4 Exactly full circular workload

| Configuration | Completed | Expired | Maximum wait | Coordination events |
| --- | ---: | ---: | ---: | ---: |
| Central | 24 | 0 | 0 | 96 |
| Global barrier | 24 | 0 | 0 | 96 |
| Local CBF | 0 | 24 | 60 | 540 |

The central and global configurations can atomically rotate a capacity-neutral batch. The local configuration requires positive receiver credit at each edge and therefore cannot initiate movement when every receiver has zero free capacity. The 24 local items remain bounded and reach the predeclared `expired_deadline` state, so the result is a liveness limitation rather than a safety violation.

This asymmetry is preserved separately as [Observation O001](../../observations/E001__OBSERVATION__FULL_RING_CIRCULATION_ASYMMETRY__v0.1__2026-07-14.md).

## 6. Interpretation

The primary E001 question receives a scoped **yes**: three local interlocks can maintain bounded occupancy and accountable progress without a central scheduler, and they contain the declared failed neighbor more locally than the global barrier.

The result is not a general performance win. The central scheduler remains a strong baseline, the slow-neighbor case did not separate the designs, and local CBF consistently spent more protocol events. The architectural value observed here is local authority and fault containment, not throughput.

The exactly full ring also exposes a constitutional choice. Strict receiver-issued credits forbid a transfer with no free destination capacity, even when a globally visible rotation would conserve every loop's occupancy. Adding an atomic exchange, escrowed circulation credit, or unrestricted bypass would change the causal contract and requires a new specification version.

## 7. Exit decision

**Proceed** to Stage B, with the following boundary:

- pressure, resistance, conductance, flow potential, and phase may be instrumented as derived observables;
- those observables may not authorize a transfer, create credit, override capacity, or bypass provenance;
- Stage B must retain the Stage A configurations as controls;
- full-ring liveness must not be retroactively added to E001 v0.1; and
- any causal circulation mechanism must be proposed and tested under a new experiment or specification version.

Proceed is chosen because the model is valid, H2 has positive comparative evidence under failure, and the circular workload terminated exactly as the frozen specification permitted. The result would change to **revise** if Stage B requires full-ring circulation as a mandatory property rather than an observable limitation.

## 8. Limitations

- The topology has only three loops and one direction.
- The baselines are experimental models, not production implementations.
- Central and global configurations have atomic batch visibility that local CBF deliberately lacks.
- Seeds affect deterministic consideration order but do not create stochastic service or workload variation.
- Service, deadlines, and faults are discrete and scheduled.
- No network, process, clock, storage, or physical pneumatic behavior is measured.
- E4 applies only to the declared simulated faults and malformed inputs; there is no independent replication.

## 9. Reproduction

After checking out the exact source commit shown above, generate the evidence tree with:

```bash
PYTHONPATH=src python tools/generate_e001_evidence.py \
  --output build/e001-canonical \
  --source-commit 81e7f859f71425bdba7603a61566f9fb47c116f9
```

Verify the preserved archive from `experiments/E001/results/raw/` with:

```bash
sha256sum --check \
  E001__CANONICAL_EVIDENCE__81e7f859f71425bdba7603a61566f9fb47c116f9.tar.gz.sha256
```
