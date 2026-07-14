# Minimal Interlock Contract

**Domain:** Conduit Barrier Field  
**Version:** v0.1  
**Date:** 2026-07-10  
**Status:** Formalized specification draft

## Purpose

An interlock is a stateful relationship between two or more Conduit Barrier Loops. It is not an ungoverned network edge. This contract defines the minimum information required to validate, admit, account for, and return feedback about a proposed transfer.

## Required fields

| Field | Purpose |
| --- | --- |
| `interlock_id` | Stable identity for the relationship and its audit trail |
| `participants` | Authorized loop identities and roles |
| `schema` | Typed representation accepted at the boundary |
| `proposal_id` | Idempotence and causal correlation key |
| `capacity_credit` | Bounded receiving headroom granted to a sender |
| `validation_state` | `accepted`, `rejected`, `revise`, `wait`, `isolate`, or `terminal` |
| `fresh_until` | Lease preventing stale feedback from authorizing progress |
| `provenance` | Source, transformations, validators, and prior obligations |
| `pressure_vector` | Relevant congestion, uncertainty, trust, and verification signals |
| `reciprocal_obligation` | Feedback or completion state owed after transfer |

## Core invariants

1. No state crosses a loop boundary without producing reciprocal state at the interlock.
2. No interlock admits more work than its bounded receiving capacity permits.
3. Every promoted state retains attributable provenance and transformation history.
4. Every `wait` state has a bounded lease, a safe degraded transition, or an explicit terminal justification.
5. Learned permeability cannot override identity, provenance, authorization, capacity, or prohibited-state rules.
6. Replayed or stale acceptance cannot authorize new progress.
7. Transfer cannot silently duplicate authority or erase an outstanding obligation.

## Minimal transition sequence

1. Sender creates a proposal with identity, type, provenance, and requested capacity.
2. Interlock verifies participant authorization and schema compatibility.
3. Receiver grants bounded capacity credit or returns pressure.
4. Validators return an admissibility state.
5. Interlock commits transfer idempotently.
6. Receiver creates the required reciprocal acknowledgment or revision obligation.
7. Credits are consumed, renewed, or released explicitly.

## Open decisions

- Whether pressure is scalar, typed, or vector-valued
- Whether validators belong to loops, interlocks, or independent rings
- Which obligations may expire safely
- How quorum rules interact with fault isolation
- How to preserve liveness without creating an unrestricted bypass

