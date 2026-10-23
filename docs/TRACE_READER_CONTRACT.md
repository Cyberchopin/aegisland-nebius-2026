# Trace reader contract

## Local trace reader (standard library only)

This is a compatibility reader for AegisLand traces that currently have no
`schema_version`. `reader_format_version` describes the output, not an upstream
schema guarantee. Python 3.11+ is recommended; no installation is required.
From this repository:

```sh
python3 -B -m trace_reader tests/fixtures/synthetic_trace.jsonl
python3 -B -m trace_reader /absolute/path/trace.jsonl --include-records
python3 -B -m unittest discover -s tests -v
```

Function entry point: `from trace_reader import read_trace`, then
`summary = read_trace("/absolute/path/trace.jsonl")`.
Only the explicitly supplied file is read: there is no runs discovery, model
call, core import, or input rewrite. JSON output contains diagnostics with
1-based physical line numbers; file-level errors use `line: null`.
Exit codes: 0 = no validation errors (warnings possible), 1 = invalid data,
2 = file I/O or command-line error. `valid` never means safe flight or successful
execution; even an empty file can be structurally valid.

The required compatibility subset is `trace_id`, nonnegative integer
`sequence`, and objects `telemetry`, `evidence`, `decision`, `command`.
Telemetry requires battery_percent [0,100] and altitude_m >= 0. Evidence requires
an evidence_id, nonnegative frame_index, and confidence/obstacle_risk/motion_risk
in [0,1]. Decisions require action, safety_level, risk_score [0,1], boolean
requires_human_approval, string-list reasons, and evidence_id matching the
embedded evidence. A supplied non-null raw_decision follows the same checks.
Command requires status; a supplied approval_id or approval_status requires both.
Optional known fields are type checked; unknown fields are allowed and preserved
in accepted records with `--include-records`. Unknown states are counted literally
with warnings and are never mapped to success. A declared schema_version emits
a compatibility warning rather than claiming support for that version.

Final decisions, raw decisions, command status, lifecycle status, and reported
execution flags have separate counters. Missing flags are explicitly missing;
raw decisions are never synthesized. Decision counts are not execution counts,
and reported flags/statuses are not proof of physical execution. Reasons count
records containing each reason. Evidence links identify their source line,
trace, sequence, evidence ID and frame index; this checks embedded associations,
not external image existence or image integrity.

Event identity is (trace_id, sequence). Semantically identical JSON objects at
the same identity are duplicate events and excluded; differing content at the
same identity is an error, with only the first valid event included. Object key
order/whitespace do not affect this comparison; array order and unknown fields
do. Approval identity is (trace_id, approval_id). Unique approvals, nonduplicate
observations, state changes, repeated-state observations, and duplicate events
are separate. State changes follow file order, including unknown states; they
are observations, not a reconstructed authorization history. Sequence starts,
gaps, and out-of-order values produce diagnostics, not fabricated events.

Invalid records are excluded from all semantic aggregates. Blank, malformed,
invalid UTF-8, duplicate-key, non-finite, oversized, and conflicting lines are
diagnosed without printing their contents. Input is streamed with a default
1 MiB line limit (including newline); `--max-line-bytes` changes it. SHA-256
covers every original byte, including invalid or oversized lines. A failed read
has no complete hash; a partial hash is labelled separately. File metadata is
checked for changes during reading, but this is not an immutable snapshot or
authenticity guarantee. Streaming I/O does not mean constant memory: event and
approval indexes, diagnostics, evidence links, and optional records grow with
input size.

The fixture and generated unittest inputs are explicitly **SYNTHETIC**. Tests
exercise parsing, CLI exit codes, counters, scoped approval deduplication,
sequence/evidence errors, unknown states, exact hashes and unchanged input.
No real trace regression has been run or claimed. This reader adds no model
integration, dependencies, or license.

