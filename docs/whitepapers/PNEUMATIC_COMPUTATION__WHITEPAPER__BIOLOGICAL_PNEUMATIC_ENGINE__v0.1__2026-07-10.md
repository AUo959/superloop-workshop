> **Superloop repository provenance:** This paper documents a recovered prototype and preserves its original status: not promoted to canon. Superloop Workshop imports it as a bounded research input for pneumatic computation, not as an inherited runtime, validated biological model, or architectural dependency.

**The Biological Pneumatic Engine**

A Pressure-Differential Model for Dialogue Processing in the Productive
Dialogue Protocol (PDP v2)

**Technical White Paper**

Aurora / ORIONCORE Workspace — Recovered Prototype Series

**Artifact:** biological_pneumatic_engine.py (SHA-256 20df6280…)

**Salvage docket reference:** P7 — Biological Pneumatic Engine Prototype
(closed 2026-07-10)

**Date:** 10 July 2026 **Status:** Recovered prototype — not promoted to
canon

**Contents**

Abstract

This paper documents the **Biological Pneumatic Engine**, a research
prototype that models conversational information processing as the flow
of a compressible fluid through a network of pressure differentials.
Rather than treating a dialogue turn as a discrete token-level
computation, the engine represents attention as pressure, cognitive load
as viscosity, and the progression of information through processing
stages as flow down a pressure gradient. Three further mechanisms are
layered on top: pneumatic logic gates modeled on microfluidic computing,
a breathing–cognition coupler that modulates processing by a simulated
respiratory phase, and a dialogue-rhythm entrainment model that
converges the system’s response cadence toward the user’s.

The prototype is grounded in four peer-reviewed research anchors, all of
which we independently verified (§9). It reaches a working, testable
form as the reference engine behind the Productive Dialogue Protocol v2
MVP (PDP v2), where a pure-Python adapter reproduces its behavior
deterministically. We present the concept, the mathematics of each
subsystem, the empirical behavior observed under test, and a candid
analysis of the gap between the metaphor’s ambition and the prototype’s
current fidelity — including a material divergence between the reference
engine and its adapter that any future productionization must resolve.

1\. Introduction and Motivation

Conventional dialogue systems process a turn as a feed-forward pass:
tokens in, logits out, with latency dominated by matrix multiplication.
This framing is powerful but offers little vocabulary for the *dynamics*
of a conversation — the sense that some exchanges flow easily while
others feel viscous, that attention concentrates and dissipates, that
two speakers fall into or out of a shared rhythm. The Biological
Pneumatic Engine is an attempt to give those dynamics a first-class
computational representation by borrowing the mathematics of fluid and
pneumatic systems.

The central analogy is simple: **information flows from regions of high
relevance-pressure to regions of low pressure, at a rate set by the
system’s viscosity and gated by attention.** This is a direct reuse of
the Hagen–Poiseuille relationship for laminar flow, repurposed so that
the “pipes” are the stages of a processing hierarchy and the “valves”
are attention weights.

The design is deliberately interdisciplinary. It draws on microfluidic
pneumatic logic (that pressure can implement Boolean computation), on
neuroscience findings that respiration measurably modulates cognition,
on speech-science work linking conversational rhythm to interaction
quality, and on a connectivity model of the cortex as a gradient from
sensory to abstract processing. The remainder of this paper treats the
prototype as an engineering artifact: what it does, how it does it, what
it gets right, and where the metaphor outruns the implementation.

2\. Research Foundations

The prototype cites four research anchors in its module docstring. Each
is a real, locatable publication; we summarize what each establishes
and, critically, how faithfully the prototype reflects it. Full
citations appear in §10.

2.1 Microfluidic pneumatic logic (Jensen, Grover & Mathies, 2007)

Jensen and colleagues demonstrated that PDMS membrane valves can act as
transistors, composing into pneumatic AND, OR, NOT, NAND, and XOR gates
and, ultimately, 4- and 8-bit ripple-carry adders — a proof that
pressure is a universal computing medium. The prototype borrows this
directly in its PneumaticLogicGate class. **Fidelity note:** the
prototype annotates its gates with a “sub-3 ms” response time attributed
to this paper. The 2007 work actually reports carry propagation through
an 8-bit adder completing within ~1.1 seconds; the millisecond figure is
not supported by the cited source and should be treated as a design
placeholder, not an empirical claim.

2.2 Breathing–cognition coupling (Heck et al., 2019; Zelano et al.,
2016)

A robust neuroscience literature shows that respiration entrains limbic
oscillations and modulates memory: recognition is more accurate during
nasal inspiration than expiration, and natural breathing synchronizes
activity in piriform cortex, amygdala, and hippocampus. The prototype’s
BreathingCognitionCoupler models this as a sinusoidal performance
modulation over a respiratory phase. **Fidelity note:** the prototype
maps inhalation exclusively to “memory encoding” and exhalation to
“retrieval.” The empirical picture is subtler — inspiration enhances
both encoding and retrieval — so the clean inhale/exhale split is a
simplification for tractability.

2.3 Dialogue rhythm entrainment (Wynn, Barrett & Borrie, 2022)

This is the prototype’s closest match to its source. Wynn et al. present
a mediated model in which rhythm-perception ability predicts
speaking-rate entrainment, which in turn predicts conversational
quality. The prototype’s DialogueRhythmEntrainment reproduces exactly
this chain: a rhythm-perception coefficient mediates a similarity-based
entrainment score, which feeds a quality estimate. The r ≈ 0.72 quality
correlation noted in the code is consistent with the published mediated
model.

2.4 Consciousness gradient (Margulies et al., 2016)

Margulies et al. established a “principal gradient” of cortical
organization running from unimodal sensory/motor regions to transmodal
association cortex (the default-mode network). The prototype borrows
this as the ordered node chain input → attention → semantic → creative →
output. **Fidelity note:** this is a metaphorical, not a mechanistic,
borrowing — the gradient supplies an intuition for ordering processing
stages, not a validated mapping onto the paper’s connectivity findings.

3\. System Architecture

The engine is composed of five subsystems coordinated by a top-level
integrator. Table 1 summarizes them; §4 gives the mathematics.

**Table 1.** *Subsystems of the Biological Pneumatic Engine.*

| **Component**                 | **Role**                                                                   | **Research anchor**     |
|-------------------------------|----------------------------------------------------------------------------|-------------------------|
| PneumaticLogicGate            | Async Boolean gates (AND/OR/NOT/XOR/NAND) with a simulated actuation delay | Jensen 2007             |
| BreathingCognitionCoupler     | Sinusoidal cognitive modulation over a respiratory phase                   | Heck 2019 / Zelano 2016 |
| PneumaticInformationProcessor | Pressure-gradient flow across a node hierarchy (Hagen–Poiseuille analogy)  | Margulies 2016          |
| DialogueRhythmEntrainment     | Rolling correlation of user vs. AI cadence → entrainment → quality         | Wynn 2022               |
| BiologicalPneumaticEngine     | Per-turn orchestration and metric aggregation                              | —                       |

Two of these subsystems are worth an early caveat. The pneumatic logic
gates are **constructed but never invoked** by any code path in the
integrator — they are latent wiring rather than an active control
surface. And the respiratory coupler’s output (“cognitive state”) is
reported as a metric but does not feed back into the flow computation.
Both are documented in the behavior inventory as migration decisions.

4\. Mathematical Model

4.1 Pressure-differential flow

The processor holds a vector of node pressures P and computes flow
between adjacent nodes using a discrete Hagen–Poiseuille analogy. For
node pair (i, i+1):

flow\[i\] = (P\[i\] − P\[i+1\]) / viscosity × mean(attn\[i\],
attn\[i+1\])

Flow is proportional to the pressure differential, inversely
proportional to viscosity, and gated by the mean attention weight of the
pair (the “valve” term). Pressures are then updated conservatively, each
node ceding or gaining 0.5 × flow × dt, so total pressure is preserved
across the transfer.

4.2 Processing latency and efficiency

Per-turn latency is a base cost adjusted by flow complexity and the
respiratory phase:

latency = max(5.0 + 0.3·Σ\|flow\| − 0.5·cos(phase), 2.0) \[ms\]

efficiency = clamp(1 − latency/50, 0, 1)

Efficiency is defined relative to a nominal 50 ms “classical” baseline.
The 2 ms floor bounds efficiency at ≤ 0.96. Note the *breathing benefit*
term: coherent respiration (via the cosine of the phase) can shave
latency, the one place respiration touches the flow model — though the
coupler’s own richer output is not used here.

4.3 Breathing–cognition coupler

The phase advances as a fixed-frequency oscillator, and cognitive state
is a baseline plus a sinusoidal modulation:

phase ← (phase + 2π·f·dt) mod 2π cognitive_state = 0.7 + 0.15·sin(phase)

Default frequency is 0.25 Hz (15 breaths/min). Task-optimal phase
windows map encoding to inhalation \[0, π\], retrieval to exhalation
\[π, 2π\], and attention to early inhalation \[0, π/2\].

4.4 Rhythm entrainment

Over a rolling 10-turn window of user and AI cadences (words/sec),
entrainment is a perception-weighted similarity, and quality is a linear
function of both:

entrainment = (1 − mean\|Δrhythm\|/5.0) × rhythm_perception (≥3 turns,
else 0)

optimal_ai_rhythm = ai·(1−k) + user·k, k = 0.3·entrainment

quality = min(0.5 + 0.4·entrainment + 0.1·rhythm_perception, 1.0)

The AI cadence converges toward the running user mean at a rate
proportional to the current entrainment — a slow, stable lock rather
than an abrupt match. **Implementation note:** the reference engine does
not clamp entrainment to \[0, 1\]; the PDP adapter does. This is one of
several small divergences catalogued in §7.

5\. Interface Contract

Each dialogue turn is processed through a single asynchronous call. The
input and output schemas are given in Table 2.

**Table 2.** *Per-turn input and output fields.*

| **Field**                         | **Direction / type**       | **Meaning**                                              |
|-----------------------------------|----------------------------|----------------------------------------------------------|
| message                           | in — str                   | Turn text (unused by the flow math; carried for context) |
| pressure                          | in — float (100.0)         | Initial relevance-pressure at the input node             |
| attention_focus                   | in — List\[float\] (len 5) | Per-node attention weights (valve settings)              |
| user_rhythm                       | in — float (4.0)           | User cadence in words/sec                                |
| response / output_pressure        | out — float                | Pressure emerging at the output node                     |
| latency_ms                        | out — float                | Modeled processing latency                               |
| efficiency                        | out — float                | 1 − latency/50, clamped to \[0,1\]                       |
| quality                           | out — float                | Conversational-quality estimate                          |
| entrainment                       | out — float                | Rhythm synchronization strength                          |
| cognitive_state / breathing_phase | out — float                | Respiratory-phase diagnostics                            |

6\. Empirical Behavior

The prototype was exercised in two configurations: the pure-Python
**fallback** adapter (no scientific dependencies) and the **external**
reference engine (NumPy). Both were driven with an identical three-turn
synthetic dialogue. Table 3 reports the last-turn metrics and the
committed validation targets.

**Table 3.** *Observed metrics vs. committed targets (3-turn synthetic
dialogue, 2026-07-10).*

| **Metric**            | **Target** | **Fallback** | **External** | **Target met?** |
|-----------------------|------------|--------------|--------------|-----------------|
| Response latency (ms) | \< 10      | 5.17         | 202.40       | Fallback only   |
| Processing efficiency | \> 0.85    | 0.897        | 0.000        | Fallback only   |
| Entrainment strength  | \> 0.70    | 0.65\*       | 0.65\*       | Approaching     |
| Cognitive boost (%)   | \> 10      | n/a          | n/a          | —               |
| PDP v2 MVP test suite | pass       | 7 / 7        | —            | Yes             |

\* Single last-turn value; the 3-turn mean entrainment is ~0.22 because
the metric requires ≥3 turns of history before it becomes non-zero.
Targets are sourced from pneumatic_validation_metrics.csv via
targets.yaml.

The headline result is the **divergence** between the two engines. The
fallback comfortably meets its latency and efficiency targets; the
reference engine misses them by nearly two orders of magnitude. The
cause is structural, not a bug in the usual sense (§7.2).

7\. Engineering Findings

7.1 Defects corrected during recovery

Two issues were fixed in the operative copy during the P7 recovery, both
verified by re-running the test suite:

1.  **Dead dependency.** The reference engine imported scipy.signal but
    never used it. Because the adapter selects the external engine only
    if its imports succeed, a missing SciPy silently forced fallback
    mode even where NumPy alone would suffice. The unused import was
    removed, so the external engine now loads with NumPy only.

2.  **Over-broad exception guard.** The adapter wrapped external-engine
    construction in a bare except Exception, which masked genuine engine
    defects as ordinary “dependency missing” fallbacks. This was
    narrowed to except ImportError so that real failures surface instead
    of disappearing.

7.2 The external/fallback divergence

The two engines are treated as interchangeable by the adapter but are
**not behaviorally equivalent**. Under the default configuration
(viscosity 0.1, five nodes, input pressure 100), the reference engine’s
latency term 0.3·Σ\|flow\| dominates: with flow ≈ ΔP/0.1, the summed
flow magnitude is large, driving modeled latency to ~200 ms and
efficiency to zero. The fallback avoids this because it derives its
gradient from attention values rather than raw node pressures, keeping
the complexity penalty small.

Neither model is obviously “correct” — they encode different assumptions
about what drives processing cost. The consequence for productionization
is concrete: **the committed validation targets are only satisfied by
the fallback, and the test suite exercises only the fallback path.** A
migration must choose a canonical latency model and either retune the
viscosity/penalty constants or revise the flow term so that the
reference engine can meet its own targets. This is tracked as queue item
p7-external-latency-divergence.

7.3 Latent and unused structure

- **Logic gates unused.** The five pneumatic gates are instantiated but
  never invoked; they represent an intended control surface that was
  never wired in.

- **Respiration under-utilized.** The coupler computes a rich
  cognitive-modulation signal, but only the raw cosine-of-phase term
  influences latency; the modulation itself is reported, not applied.

- **Wall-clock simulation.** Gates and the processor use real
  asyncio.sleep calls to “simulate” pneumatic delay, making turn time
  scale with the modeled duration. A production version should use
  simulated time.

8\. Disposition and Migration Path

Under the salvage docket (P7), the owner selected the **root
recovered-prototype archive** lane. A pristine, hash-verified snapshot
(SHA-256 20df6280…, byte-identical to the original docket evidence) is
frozen alongside a behavior inventory that serves as the required
precursor for any future code migration. The prototype is explicitly
**not promoted to canon**.

Should the engine later be routed to a runtime lane (for example,
CloudBank), the recommended sequence is:

3.  Resolve the external/fallback latency divergence and adopt a single
    canonical model.

4.  Decide the fate of the unused logic gates — wire them into flow
    control or remove them.

5.  Replace wall-clock delays with simulated time and add clamping
    parity between engines.

6.  Extend the test suite to cover the external engine, not just the
    fallback.

7.  Re-validate against the committed metrics before any canon
    promotion.

9\. Verification and Provenance

Consistent with the workspace’s evidence-over-assumption principle,
every empirical claim in this paper is backed by a repeatable action.
The engine metrics in Table 3 come from direct execution on 2026-07-10;
the “7/7 tests pass” claim comes from running the PDP v2 MVP suite; the
artifact hash was verified against the docket evidence before any
modification. The four research anchors in §2 were each located and
characterized via literature search (§10) rather than reproduced from
the code’s own annotations — which is how the two fidelity discrepancies
(the Jensen timing figure and the Heck inhale/exhale split) were caught.

10\. References

8.  Jensen, E. C., Grover, W. H., & Mathies, R. A. (2007).
    Micropneumatic digital logic structures for integrated microdevice
    computation and control. *Journal of Microelectromechanical Systems,
    16(6), 1378–1385.*
    <https://groverlab.org/assets/pneumatic-logic.pdf>

9.  Heck, D. H., Kozma, R., & Kay, L. M. (2019). The rhythm of memory:
    how breathing shapes memory function. *Journal of Neurophysiology,
    122(2), 563–571.*
    <https://journals.physiology.org/doi/pdf/10.1152/jn.00200.2019>

10. Zelano, C., et al. (2016). Nasal respiration entrains human limbic
    oscillations and modulates cognitive function. *Journal of
    Neuroscience, 36(49), 12448–12467.*
    <https://www.jneurosci.org/content/36/49/12448>

11. Wynn, C. J., Barrett, T. S., & Borrie, S. A. (2022). Rhythm
    perception, speaking rate entrainment, and conversational quality: A
    mediated model. *Journal of Speech, Language, and Hearing Research,
    65(6), 2187–2203.*
    <https://pubs.asha.org/doi/10.1044/2022_JSLHR-21-00293>

12. Margulies, D. S., et al. (2016). Situating the default-mode network
    along a principal gradient of macroscale cortical organization.
    *PNAS, 113(44), 12574–12579.*
    <https://www.pnas.org/doi/10.1073/pnas.1608282113>

Appendix A. Artifact Locations

| **Artifact**        | **Repository path**                                                                             |
|---------------------|-------------------------------------------------------------------------------------------------|
| Frozen snapshot     | archives/recovered_prototypes/biological_pneumatic_engine/biological_pneumatic_engine.py        |
| Recovery record     | archives/recovered_prototypes/biological_pneumatic_engine/RECOVERY_RECORD\_\_2026-07-10.md      |
| Behavior inventory  | archives/recovered_prototypes/biological_pneumatic_engine/BEHAVIOR_INVENTORY\_\_2026-07-10.md   |
| Operative engine    | projects/Aurora_New_11_9/04_DEVELOPMENT/Python_Modules/biological_pneumatic_engine.py           |
| PDP v2 adapter      | projects/Aurora_New_11_9/04_DEVELOPMENT/Python_Modules/pdp_v2_mvp/core/pneumatic_engine.py      |
| Validation targets  | projects/Aurora_New_11_9/03_SPECIFICATIONS/Bootstrap_Standards/pneumatic_validation_metrics.csv |
| Salvage docket (P7) | reports/analysis/salvage_docket\_\_2026-06-12.md                                                |

*This document is a technical description of a research prototype. It
does not assert that the prototype’s biological or cognitive analogies
are validated mechanisms; claims of fidelity are bounded by §2 and §7.*
