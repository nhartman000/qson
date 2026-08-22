# QSON Provenance and Scope

**Author:** Nicholas Hartman / American Milestone Inc.

This document records the current canonical baseline for the `.qson` execution-trace layer in the MG8 file family.

## Established baseline

QSON is the immutable/auditable runtime trace artifact that records realized execution events.

The baseline includes:

- unique event-level `trace_id` for every attempted gate execution,
- optional `run_id` to group related events,
- deterministic event `sequence` within a run,
- linkage to `.g8son` `file_id` and `gate_id`,
- linkage to input/output `.gst` `state_id` values,
- gate results `PASS`, `FAIL`, and `INTERMEDIATE`,
- selected action/branch recording,
- actor/evaluator attribution,
- append-only override/correction semantics,
- optional evidence and metadata references,
- optional stronger cryptographic integrity fields.

## Identity semantics

The established identity relationship is:

```text
file_id != gate_id != trace_id
```

A repeated execution of the same gate creates a new trace event.

## Immutability semantics

QSON's base immutability claim is semantic/audit-oriented: prior execution events are not silently rewritten.

Corrections, reviews, and overrides are represented as later events referring to the earlier event.

The base specification does not claim cryptographic immutability merely because a file uses the `.qson` extension.

## TCTA interoperability

When a QSON event records a realized state transformation, it may preserve the runtime evidence necessary to reconstruct the transformation tuple:

`SR_in -> T -> SR_out + metadata/evidence`

This aligns with the TCTA CIIU trace structure while keeping QSON and TCTA distinct in purpose.

## Acronym boundary

No authoritative expanded phrase for `QSON` has been established in the current repository baseline. The name is therefore preserved as `QSON` / `.qson` without inventing an expansion.

## Relationship to the MG8 family

```text
.gst    structured state/context
.g8son  bounded conditional gate/operator definitions
.ork    sequencing/orchestration
.qson   immutable/auditable realized execution trace
.mg8    bounded execution unit
.mg8pk  package/composition layer
```

## Scope boundary

This repository establishes the generic `.qson` trace contract. It does not fully specify `.gst`, `.g8son`, `.ork`, `.mg8`, or `.mg8pk`, and it does not prescribe a mandatory cryptographic sealing implementation unless a later profile explicitly does so.
