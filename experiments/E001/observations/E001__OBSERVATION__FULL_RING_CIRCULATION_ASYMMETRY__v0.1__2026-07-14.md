# E001 Observation O001 — Full-Ring Circulation Asymmetry

**Artifact class:** Emergent observation  
**Version:** v0.1  
**Date:** 2026-07-14  
**Status:** Seed  
**Evidence class:** E0  
**Originating experiment:** `SW.EXPERIMENT.E001`  
**Source commit:** `81e7f859f71425bdba7603a61566f9fb47c116f9`

## Observation before interpretation

In canonical scenario S6, every loop begins at capacity with eight processed items waiting for its clockwise neighbor. For all three seeds:

- central scheduling completed all 24 items with 96 coordination events;
- the global barrier completed all 24 items with 96 coordination events; and
- local CBF completed no items, emitted 540 coordination events, waited 60 ticks, and expired all 24 items accountably.

The relevant interval is simulation ticks 0–60 in runs:

- `local_cbf__circular_wait__seed-17`;
- `local_cbf__circular_wait__seed-29`; and
- `local_cbf__circular_wait__seed-43`.

The canonical traces are preserved in the [E001 evidence archive](../results/raw/E001__CANONICAL_EVIDENCE__81e7f859f71425bdba7603a61566f9fb47c116f9.tar.gz), and the extracted machine summaries are in the [summary directory](../results/summary/).

## Ordinary explanations

The most direct explanation is representational rather than thermodynamic:

- central and global configurations can commit an atomic batch whose outgoing movements create the capacity needed for incoming movements;
- local CBF evaluates each edge through strict receiver-issued free-capacity credit;
- with occupancy 8 of 8 everywhere, every receiver advertises zero free capacity; and
- no first local transfer can create the vacancy needed by the next transfer.

Other explanations considered:

- **Seed dependence:** unlikely within E001; all three seeds produced identical terminal behavior.
- **Nondeterminism:** rejected by the repeated canonical matrix; traces and summaries matched byte for byte.
- **Event-order artifact:** still plausible in the broader sense that local commits are sequential rather than simultaneous, but rotating consideration order did not change the result.
- **Implementation defect:** no hard invariant failed, ledgers balanced, and the behavior follows the frozen credit rule.

## Noncanonical perturbation

A local exploratory perturbation removed one preloaded item, leaving one free slot in the field. This was not part of the canonical matrix and was run only to discriminate the boundary.

| Configuration | Admitted | Completed | Maximum wait |
| --- | ---: | ---: | ---: |
| Central | 23 | 23 | 0 |
| Global barrier | 23 | 23 | 0 |
| Local CBF | 23 | 23 | 1 |

The perturbation suggests a sharp zero-vacancy circulation cliff: one free slot is sufficient for the current local protocol to drain the ring. Because the perturbation was not frozen in advance and used the local exploratory runtime, it remains E0 context and is not promoted as E001 evidence.

## Possible significance

The result may distinguish two meanings of capacity:

1. **static free capacity**, which the current local credit represents; and
2. **capacity released by a committed cyclic exchange**, which requires multi-edge coordination or escrow.

A pressure-like observable could detect the symmetric fully saturated state, but detection alone cannot safely authorize movement. Any mechanism that converts that signal into a cyclic swap would be a new causal primitive rather than passive pneumatic instrumentation.

## Smallest proposed discriminating tests

1. Freeze a vacancy sweep from zero through three free slots while holding total work and topology constant.
2. Repeat the sweep on four- and five-loop rings to separate three-node symmetry from zero-vacancy behavior.
3. Compare strict local credit with an explicitly specified cyclic escrow protocol.
4. Instrument pressure potential as a read-only signal and verify that it predicts the cliff without changing any transition.

These tests belong in a new experiment or E001 v0.2. They must not alter the canonical E001 v0.1 result.
