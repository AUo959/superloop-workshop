# Superloop Concept Registry

This registry is the identity and status index for foundational Superloop concepts. Status changes require evidence and should be reviewed through a pull request.

| Identifier | Name | Status | Evidence | Role |
| --- | --- | --- | --- | --- |
| `SW.CONCEPT.CBL` | Conduit Barrier Loop | Formalized | E1 | Atomic recurrent unit |
| `SW.CONCEPT.INTERLOCK` | Regulated Interlock | Formalized | E1 | Shared barrier–conduit transition surface |
| `SW.CONCEPT.CBF` | Conduit Barrier Field | Formalized | E1 | Distributed topology of interlocking CBLs |
| `SW.CONCEPT.FIELD_THERMODYNAMICS` | Field Thermodynamics | Seed | E0 | Pressure, flow, resistance, capacity, and equilibrium operating model |
| `SW.CONCEPT.PNEUMATIC_COMPUTATION` | Pneumatic Computation | Formalized | E1 | Computation through pressure-differential mechanisms |
| `SW.PROTOTYPE.BPE` | Biological Pneumatic Engine | Prototyped / archived input | E2-limited | Recovered PDP v2 prototype; not a Superloop runtime dependency |
| `SW.BRIDGE.CBF_PNEUMATIC` | CBF–Pneumatic Bridge | Formalized | E1 | Controlled synthesis: CBF constitution plus optional pneumatic dynamics |
| `SW.EXPERIMENT.E001` | Three-Ring Bounded Flow | Completed | E4-scoped | Repeated 72-run Python 3.13 comparison; result is limited to the declared three-ring model |
| `SW.EXPERIMENT.E002` | Noncausal Pneumatic Instrumentation | Completed / Narrow | E4-scoped | Exact typed telemetry retained; fixed scalar flow law did not meet diagnostic usefulness threshold |

## Naming rule

`Superloop` is the project and workshop identity. It is not currently a synonym for CBL, CBF, pneumatic computation, or any specific runtime.

## Provenance rule

Artifacts may preserve prior workspace labels for historical accuracy. Those labels do not transfer external authority into this registry.
