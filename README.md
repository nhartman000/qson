# QSON — `.qson` Execution Trace

**QSON** is Nicholas Hartman / American Milestone Inc.'s immutable/auditable execution-trace layer within the MG8 file family.

A `.qson` record captures **what actually happened during execution**. It links the state presented to a gate, the gate definition that was attempted, the runtime execution identity, the result, the selected continuation, and the resulting state when one is produced.

> The repository does not currently assign an expanded phrase to the acronym `QSON`; this documentation preserves the established `.qson` name without inventing one.

## Role in MG8

```text
.gst state/context
      ↓
.g8son gate/operator
      ↓
PASS / FAIL / INTERMEDIATE
      ↓
.ork routing / sequencing
      ↓
.qson realized execution event
```

At `.mg8` unit scope, QSON is the audit/provenance layer for realized execution.

## Identity model

QSON preserves the identity distinction established by G8SON:

```text
file_id != gate_id != trace_id
```

- `file_id` identifies the `.g8son` file containing the gate definition.
- `gate_id` identifies the gate definition.
- `trace_id` identifies **one attempted execution** of that gate.

Repeated execution of the same gate MUST produce a new `trace_id` for every attempt.

A larger run may also carry a `run_id` or equivalent pipeline/session identity so multiple gate events can be grouped without collapsing their event identities.

## Core event relationship

A QSON event should make this chain reconstructable:

```text
input .gst state
      ↓
file_id + gate_id
      ↓
unique trace_id
      ↓
operation / transform attempt
      ↓
PASS / FAIL / INTERMEDIATE
      ↓
selected action / branch
      ↓
resulting .gst state (when produced)
```

## Append-only / immutable semantics

QSON is intended as an **append-only execution record**.

A previously committed event should not be silently rewritten to change what the system claims occurred. If an event must be corrected, superseded, reviewed, or overridden, the correction should be represented by a new trace event linked to the prior event.

This semantic immutability does **not** by itself claim a particular cryptographic ledger implementation. Hash chaining, signatures, Merkle structures, or external notarization may be added by profiles that explicitly define them.

## Minimum event fields

The canonical minimum event model includes:

- `trace_id`
- `run_id` when events belong to a larger run
- execution `sequence`
- source `.g8son` `file_id`
- `gate_id`
- input `.gst` `state_id`
- gate `result`: `PASS`, `FAIL`, or `INTERMEDIATE`
- selected `action` / branch
- resulting `state_id` when a new state is produced
- actor/evaluator identity or type where relevant
- timestamp and/or deterministic execution index
- metadata/evidence references when required

## QSON and overrides

An override does not erase the original gate result.

Conceptually:

```text
trace A: gate result = FAIL
       ↓
trace B: authorized override of trace A
       ↓
trace C: continuation executed under override
```

This preserves the difference between the system's original evaluation and the later decision to supersede it.

## Relationship to TCTA / CIIU

Where MG8 is used to record a realized state transformation, a QSON event can carry the evidence required to reconstruct the transformation relationship represented by a TCTA CIIU:

```text
SR_in → T → SR_out + metadata/evidence
```

QSON is the runtime trace artifact; it is not itself the complete TCTA algebra.

## Repository structure

- [`spec/qson_v1.md`](spec/qson_v1.md) — canonical QSON v1 trace specification
- [`schema/qson.schema.json`](schema/qson.schema.json) — minimum interoperable event-ledger schema
- [`examples/basic.qson`](examples/basic.qson) — minimal trace example
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — execution and provenance architecture
- [`docs/PROVENANCE.md`](docs/PROVENANCE.md) — scope and provenance baseline

## Status

This repository establishes the generic QSON trace contract. Domain-specific evidence payloads, cryptographic sealing, storage engines, retention policies, and external notarization belong to explicit profiles rather than being assumed by the base format.
