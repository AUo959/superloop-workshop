# Source Implementations

No reference runtime has been adopted yet.

The first implementation should be a deterministic discrete-event simulator with:

- explicit CBL state machines;
- stateful interlocks;
- bounded queues and capacity credits;
- simulated rather than wall-clock time;
- machine-readable transition traces;
- seeded fault injection;
- interchangeable centralized, global-barrier, and local-interlock schedulers.

Language and framework selection should follow the E001 experiment design rather than precede it.

