# Devpost copy — workbench revision

Prepared for owner review. Use only after publishing this build and confirming
the video/screenshots match it. This document has not been posted to Devpost.

## Project name

AegisLand — evidence review for Physical AI

## Short description

Trace a simulated drone decision back to its visual evidence, approval state and
source record in an interactive review workbench.

## Inspiration

When a drone simulation changes from returning home to avoiding an intrusion,
the next question is why. Which observation changed? Was approval required?
Does an execution flag describe a simulated action or prove hardware moved?
AegisLand makes those questions inspectable through the recorded evidence.

## What it does

The workbench connects three saved OpenCV simulation replays to 230 original
trace events. An operator can compare the moment before and after an intrusion,
inspect a pending approval, or locate an enhanced observation under low light.
Selecting an event seeks to its video frame and shows its decision, recorded
reason, evidence ID, approval state and execution flags.

Public provenance summaries retain source identities and validation counts while
omitting local filesystem paths, commands and environment configuration.
Each deterministic check points to an original source line and the full trace's
SHA-256. The operator can inspect the exact record and export the review as JSON.
The interface distinguishes simulated execution from physical proof.

The model adapter is a separate bounded review path: NVIDIA Nemotron on Nebius
may select a supplied evidence line and an allowed check; local code validates
the response before evaluating the recorded facts. Real hosted inference has
succeeded, but successful live citation-grounded review remains unverified.
The working offline interface displays deterministic checks, not model results.

## How we built it

Python's standard library validates JSONL, hashes source evidence, runs review
checks and serves the local interface. HTML and JavaScript provide scenario
selection, event inspection, video frame seeking and JSON export. A pinned
importer checks upstream Git blob identities, original trace provenance and
display-video hashes before generating the workbench.

The Nebius adapter uses `nvidia/nemotron-3-super-120b-a12b` through Token Factory.
Evidence packets contain at most 32 source records and 32 KiB. The new window
interface retains original line numbers and the complete source-file hash while
reviewing a small segment of a longer simulation. Credentials stay in the
environment; the offline workbench needs none.

## What we verified

All 230 imported simulation records pass the trace reader. Eighty-three automated tests
passed during this revision, covering parsing, citations, request isolation,
source-window boundaries, embedded-data escaping and local video byte ranges.
Browser checks confirmed the intrusion transition, pending approval, enhanced
observation and seeking to sequence 38 at 2.533 seconds. All 29 retained historical
Nebius evaluation files remain unchanged.

Two historical requests returned the expected NVIDIA model through Nebius with
HTTP 200. Neither established a successful citation-grounded review. The later
request exhausted its 1,024-token completion allowance in reasoning and ended
with `finish_reason=length`. These are integration diagnostics, not a model
accuracy or latency benchmark. The original authentication failure is retained.

## Challenges and lessons

The main integration challenge was preserving trustworthy citations while moving
from tiny constructed examples to longer saved simulation traces. We validate
the complete source first, then project a bounded window without renumbering its
events. A response citing a different line or evidence ID is rejected.

We also learned that reaching a model is different from obtaining a usable
review. The workbench labels its deterministic results explicitly and keeps
failed live requests separate from completed evidence checks.

## Existing work and new contribution

The OpenCV perception stack, deterministic planner and recorded simulation runs
are prior AegisLand work. This revision reuses saved evidence from
`aegisland-opencv-2026` at `de93d5a`, generated with the core pinned to `eda23d3`.
They are synthetic simulation, not newly recorded hardware footage.

The Nebius competition contribution includes the trace reader, bounded provider
adapter, citation validation, constructed baseline evaluation and guarded runtime
diagnostics. This revision adds source-line windows, verified import of existing
simulation evidence and the interactive review workbench. No core module or model
weight is bundled. Original integration code is MIT licensed; external assets,
models and services retain their own rights boundaries.

## What's next

Confirm a supported hosted-model configuration, complete a separately authorized
live citation check, and evaluate independently labeled simulation windows against
the deterministic baseline. The current build does not establish a model quality
advantage, real-world safety improvement or autonomous hardware operation.

## Tool feedback

Token Factory returned model identity, usage and finish metadata that helped
diagnose a truncated review. Clear model-specific examples for reasoning controls
would make small structured extraction tasks easier to configure. This build
does not claim that a hosted reasoning switch has been verified.

## Built with

Python, HTML, JavaScript, JSONL, SHA-256, unittest, Nebius Token Factory,
NVIDIA Nemotron 3 Super. OpenCV simulation/perception is disclosed reused work.

## Links and testing instructions

- Public source: https://github.com/Cyberchopin/aegisland-nebius-2026
  — publish and verify the new revision before updating the entry.
- Existing entry: https://devpost.com/software/aegisland-evidence-review-for-physical-ai
- Video: retain the existing URL only if its content still matches the entry;
  replace it with the actual public URL after recording the updated demonstration.
- Testing: follow README.md in this bundle; Python 3.11+, no API key required.
- Suggested track: Physical AI, reflecting the simulation review modules.
- Complete personal/team fields privately in Devpost. Disclose AI assistance
  accurately if requested by the current form.
