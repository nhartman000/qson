# QSON Architecture

**Nicholas Hartman / American Milestone Inc.**

## 1. Position in the MG8 file family

```text
.gst state/context
      ↓
.g8son bounded gate/operator
      ↓
PASS / FAIL / INTERMEDIATE
      ↓
.ork routing / sequencing
      ↓
.qson realized event ledger
```

QSON records execution after the runtime has attempted or completed an operation. It does not replace the state, gate, or orchestration layers.

## 2. Provenance chain

A normal gate-execution trace is reconstructable as:

```text
input_state_id
      ↓
file_id
      ↓
gate_id
      ↓
trace_id
      ↓
result
      ↓
action / branch
      ↓
output_state_id
```

This creates a direct provenance link from input state through gate execution to resulting state.

## 3. Event versus run identity

One larger execution may contain many events:

```text
run_id
  ├── trace_id A
  ├── trace_id B
  └── trace_id C
```

`run_id` groups events. It does not replace event identity.

## 4. Ordered ledger

Each event should carry a deterministic `sequence` within its run.

```text
run-001 / sequence 1
run-001 / sequence 2
run-001 / sequence 3
```

This preserves execution order independently of wall-clock timestamp precision.

## 5. Append-only correction model

QSON's immutability is semantic and audit-oriented:

```text
original event
      ↓
correction / override event references original
      ↓
subsequent execution continues from explicit new decision
```

Historical events remain visible.

An override therefore records a new decision rather than rewriting the gate's original result.

## 6. Optional integrity strengthening

The base format may be strengthened with:

- `previous_event_hash`
- `event_hash`
- signatures
- Merkle roots
- external timestamp/notarization

These fields are optional until a cryptographic QSON profile defines canonical serialization and verification rules.

## 7. CIIU interoperability

For a realized state transformation, QSON can carry runtime evidence corresponding to:

```text
SR_in
  ↓
Transform T
  ↓
SR_out
  ↓
metadata / evidence M
```

which aligns with the TCTA transformation record:

`CIIU = (SR_in, T, SR_out, M)`

QSON provides the event provenance for the realized transform; TCTA provides the broader trajectory algebra.

## 8. Failure and review events

Not every QSON event represents a successful state transition.

The ledger may also record:

- failed gate attempts,
- INTERMEDIATE outcomes,
- runtime errors,
- external-input arrivals,
- review events,
- overrides,
- corrections.

This is important because an audit record that contains only successful transitions cannot reconstruct the actual decision path.
