# Stage B3 — Nebius × NVIDIA submission readiness

## Current authoritative status

Submission package finalized locally: the README is current, the integration
has a root MIT license plus verified license boundaries, and `docs/submission/`
contains the Devpost text, evidence table, executable offline-demo instructions,
screenshot checklist and exact personal submission steps. The owner authorized
license selection; missing-license statements below are historical. The source
is not yet committed/pushed by this work, and no video/screenshots/Devpost entry
have been recorded, uploaded or submitted automatically.

Run `python3 -B scripts/demo_runbook.py --output-dir /tmp/aegisland-recording-01
--interactive` as one command, choosing a fresh output directory. It operates
only offline, generates screenshot-ready HTML/JSON and checks preservation.
The user must record/edit/upload media, confirm rights/eligibility, approve or
perform publication of the reviewed local branch, and submit the completed
Devpost entry. See [personal checklist](submission/SUBMISSION_CHECKLIST.md).
The deadline remains October 30, 2026, 10:00 AM PDT. Do not make a new live call
before Nebius confirms reasoning-control support and new authorization is given.

B4 supersedes the candidate-only status below: owner-run attempt 003 returned
HTTP 200, finish `length`, with all 1,024 completion tokens reported as reasoning.
The review remains `not_verified`. **74 offline tests pass**; all 24 prior
evidence artifacts and all three consumed guards are unchanged. NVIDIA documents
non-thinking and low-effort settings, but exact Nebius compatibility is unverified.
The offline request specification is tested and blocked from transmission. No
fourth attempt is prepared. See [B4 remediation](B4_REASONING_REMEDIATION.md).
Runtime integration is demonstrated; citation grounding is not. Older candidate
statements below are historical. Submission deadline remains October 30.

Attempt `b3-smoke-003` is now prepared as a candidate with independent guard and
evidence paths and 1,024 maximum output tokens. **70 offline tests pass; all
20 prior evidence files remain unchanged.** No third live request was made or
authorized for execution. The prior two attempts remain consumed. See
LIVE_API_GATE.md for the command, cost estimate and exact required final GO.
Submission drafts are in `docs/submission/`; they remain unpublished and disclose
the unverified live review. The missing repository license remains an owner action.

**Real Nebius-hosted NVIDIA integration: demonstrated. Evidence-grounded live
review: not verified.** Submission target: October 30, 2026, 10:00 AM PDT
(17:00 UTC). This is a prototype, not a completed or certified Physical AI system.

| Evidence | Observed outcome |
| --- | --- |
| `evaluation/results/live_smoke.json` | Attempt 001: HTTP 401, allowance consumed |
| `evaluation/results/live_smoke_002.json` | Attempt 002: HTTP 200, returned NVIDIA Nemotron 3 Super, review `not_verified` |
| Attempt 002 usage | 324 input + 256 output = 580 tokens; 2,304.33 ms; estimated $0.0003276 |
| Both persistent guards | Consumed, preserved; no retry authorized |
| `evaluation/b3/offline_tests.json` | 62 offline tests passed; zero failures/errors/skips; all 11 prior evidence files unchanged |

The returned model is `nvidia/nemotron-3-super-120b-a12b`, served by
`https://api.tokenfactory.nebius.com/v1/chat/completions`. This satisfies the
technical runtime-integration demonstration, not overall entry eligibility.
The prior regional 401's precise authentication cause remains unproven.

B3 found that attempt 002 exhausted its 256 output-token limit; truncation or
reasoning-budget exhaustion is plausible, not established. Finish reason, raw
answer and reasoning-token details were not retained. No successful citation
validation can be inferred or reconstructed. The current implementation still
uses 256 output tokens and a 15-second socket timeout with no retries.

B3 adds future allowlisted finish reasons, numeric token details and safe failure
codes. It stores no raw model/ reasoning text. Both guards and every pre-existing
evidence artifact remain unchanged. No third attempt or live API call was made.
See [B3 failure analysis](B3_FAILURE_ANALYSIS.md) for facts, hypotheses, parser
tests and the **unimplemented** proposal to increase only the output allowance to
1,024 on a separately authorized request. This proposal does not promise success.

## Deadline priorities and remaining blockers

1. Decide whether to authorize a single future verification with additional output
   headroom. No new attempt is currently authorized. Preserve strict citations;
   if no verified review is obtained, disclose that limitation in the submission.
2. Assemble the evidence package around the retained live model/usage/status and
   B3 hashes. Label the six-scenario baseline/mock evaluation as synthetic and
   offline; never present mock results as NVIDIA model quality measurements.
3. Record a short demo showing actual key modules in operation. Use at least one
   minute of module operation within the Physical AI video, preferably under
   three minutes total. Clearly distinguish real runtime evidence from the
   deterministic offline review demonstration and its unverified live result.
4. Finalize README/setup/judging instructions, license and core/data provenance.
   No real core simulation trace regression has been run here. Core baseline
   remains `eda23d3`; no core code or other competition repository was modified.
5. Prepare Devpost fields: track, problem, audience, architecture, explicit NVIDIA
   and Nebius usage, significant changes from existing AegisLand, tool feedback,
   public source and video links. Confirm registration, entrant eligibility,
   Physical AI track fit and judging access against the official rules.

No deployment, publishing, push, merge or third inference should happen without
the relevant new owner authorization. The next priority is the NVIDIA submission
package, not model training or added infrastructure.

## Historical B1/B2 notes — superseded by the current status above

Current state: attempt 001 returned HTTP 401 and consumed its guard; its JSON
and guard are preserved byte-for-byte. Attempt `b2-smoke-002` is prepared with
independent guard/evidence paths and the documented global Token Factory
endpoint. **55 offline tests pass; zero new live requests.** Separate final
owner authorization is required before execution. See the current-state section
of LIVE_API_GATE.md and `evaluation/results/second_attempt_preparation.json`.
Older status statements below are historical. Runtime eligibility remains
undemonstrated because attempt 001 returned no model result.

Latest authorization update: the owner approved the mutually exclusive
`--owner-accepts-no-account-cap` mode for one synthetic request, waiving the prior
account-side-cap condition for that request only. The owner requires separate
final GO before execution. Implementation-only work is complete: **47 offline
tests pass**, payload and persistent guard are unchanged, and zero live requests
were made. The API key is still not visible in the active execution environment.
The exact pending command and authorization terms are in LIVE_API_GATE.md.
Earlier test counts and hard-cap requirements below describe prior stages.

Local checks updated 2026-10-22. Branch: `codex-b/stage-b1-nebius`.
Status: local integration tested; live API and competition readiness unverified.

2026-10-22 live authorization update: owner authorized exactly one attempted
synthetic inference, no retries, conditional on private credentials and a verified
$1 total billable ceiling. Authorization remains unconsumed. Offline checks find
`NEBIUS_API_KEY` absent, and the dollar ceiling is not yet established. No API
attempt was made. See `evaluation/results/live_verification_gate.json` and
LIVE_API_GATE.md. Earlier references below to pending authorization are historical;
the current blockers are the conditions attached to the granted authorization.

## B2 result

Continuing on the dedicated B1 branch preserves the existing uncommitted B1
implementation. B2 adds six synthetic trace scenarios, a deterministic no-model
baseline, offline comparison, labeled safe fallback, provider refusal handling,
a disabled live smoke command and machine-readable local/CI evidence.

Observed locally: **44 tests passed**, zero failures/errors/skips. Baseline exact
matches: **6/6**; B1 first-event mock: **1/6**. These are synthetic harness results,
not NVIDIA outputs or model benchmarks. No real API verification occurred.
See [MODEL_EVALUATION.md](MODEL_EVALUATION.md) for the contract and limitations,
[LIVE_API_GATE.md](LIVE_API_GATE.md) for authorization and cost controls, and
`evaluation/results/` for JSON evidence with source/input hashes.

```sh
python3 -B -m run_local_checks
python3 -B -m live_smoke
```

The second command is disabled by default and makes no request. Credentials
remain an external prerequisite. Minimum owner actions: explicitly authorize
one potentially billable synthetic request, privately inject `NEBIUS_API_KEY`,
and confirm regional model access/quota/pricing. Only then use the fully gated
command documented in LIVE_API_GATE.md. No permission is assumed from this plan.

`python3 -B -m live_smoke --preflight` now checks prerequisites offline. Its
retained result in `evaluation/results/offline_preflight.json` confirms a valid
synthetic trace and missing credential/configuration prerequisites. Even when
live flags are supplied, preflight performs no API request.

Provider failure is either a redacted error (strict adapter), an explicitly
labeled baseline fallback (safe review harness), or `not_verified` (live smoke).
None permits hardware action or claims successful model inference.

## Official requirements

[Official rules](https://nebiusglobalaihackathon.devpost.com/rules), sections 1–4,
6 and 8: deadline October 30, 2026, 10:00 AM PDT (17:00 UTC); Grand Prize
$20,000. Eligibility requires majority age, permitted residency, and no excluded
organizer/judge affiliation or conflict. Entrant eligibility remains unconfirmed.

Technology requires an NVIDIA open-source model plus a runtime Token Factory call
or execution on Nebius AI Cloud. Mock tests do not qualify. Physical AI permits
module footage without hardware; the video needs at least one minute of operation
and should be under three minutes. Public source, an open-source license, setup
instructions, English materials, track selection, tool feedback, and disclosure
of significant changes to an existing project are required. Physical AI has a
demo-URL exception, but judging access must be arranged. Recheck rules before entry.
Serverless simulation is described in the Physical AI track; confirm with the
organizer whether the Token Factory-only replay approach satisfies that track.

## Supported model and endpoint

Selected candidate: `nvidia/nemotron-3-super-120b-a12b`.
[Nebius's example](https://nebius.com/services/token-factory/nemotron) supplies
that exact model ID and `https://api.tokenfactory.us-central1.nebius.com/v1/`.
[Nebius's model announcement](https://nebius.com/blog/posts/nemotron3-super-now-available)
describes text input/output and open weights, datasets and training recipes.
This establishes documented support, not account-level availability or a successful
request. Verify the model's current license/terms before submission; do not assume
open weights alone imply an OSI license. This integration consumes text evidence,
not video or images.

## Inspection and provenance

Starting commit: `efd35ca`. No AGENTS.md found in this repository. Existing files:
`trace_reader.py`, a synthetic JSONL fixture, 16 unittest cases, and
`.github/workflows/tests.yml` (Python 3.12, unittest discovery, read-only contents
permission). The reader validates the compatibility subset, deduplicates events,
preserves physical line references, hashes source bytes, and keeps recorded
decisions separate from execution claims. It is imported unchanged.

[Core reference](https://github.com/Cyberchopin/aegisland-agentic-vision) describes
the simulation and evidence pipeline. This repository's README pins core baseline
`eda23d3`; B1 does not validate that baseline against a generated real trace.
No core module was copied or changed, and no other competition repository was
modified. The new contribution is the provider adapter, constrained review loop,
offline tests and this readiness documentation.

## Smallest meaningful loop

1. Read an explicit trace through the existing reader; reject invalid/empty traces.
2. Project at most 32 accepted events into a packet capped at 32 KiB. Include
   event identity, line, evidence ID/frame, risk values, approval metadata and
   reported execution flags. Omit arbitrary extensions and free-text reasons.
3. Ask the model to select one event and one allowed check: `approval_gate` or
   `execution_claim`. Reject malformed output, unknown checks, extra keys,
   duplicate JSON keys and citations that do not match the packet.
4. Evaluate the selected check locally and emit the cited observation, source
   SHA-256, reader diagnostics and deterministic finding. Model selection thus
   changes which evidence/check is evaluated, without introducing model-written
   factual explanations.

This is a single-turn simulation-trace review loop, not a simulator controller or
new perception pipeline. It performs no resimulation, image verification, core
policy changes, hardware operation or inferred physical-success scoring.
`no_recorded_gate_conflict` is a narrow consistency result, not a safety verdict
or proof of valid approval history. Missing execution flags remain null.
Unknown reader states remain visible through diagnostics. IDs/status strings are
untrusted inputs; schema/citation enforcement limits output authority, but does
not establish that the model chose the best event. Reader memory still grows
with the input file before the review packet limit is checked.

## Run locally — no credentials, network or costs

Python 3.11+; standard library only:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B -m nebius_review tests/fixtures/synthetic_trace.jsonl
python3 -B -m trace_reader tests/fixtures/synthetic_trace.jsonl
```

Historical B1 result: 27 tests passed (16 existing + 11 integration tests). Mock CLI
completed on the SYNTHETIC fixture. The suite tests hash/input preservation,
model-dependent check selection, approval conflicts, missing flags, projection,
invalid traces/citations/output, mocked HTTP payload/auth/timeout, response limits,
redacted failures, refusal of redirects and the explicit live-call gate.
CI now runs `run_local_checks` and uploads the resulting JSON; no hosted CI run is claimed.
HTTP mocks establish adapter behavior only. No real API, GPU, benchmark, physical
flight, or real trace regression was run. The default mock chooses the first
event deterministically; it is not NVIDIA model inference.

## Live verification — pending authorization

`NEBIUS_API_KEY` was absent in the active environment. Exact prerequisites:
a Token Factory account, an API key authorized for the selected regional model,
available quota/credits, network access, and explicit permission for a potentially
billable request plus upload of the projected evidence. Do not paste keys into
source or command history; inject through your shell/secret manager. No dotenv
loader or credential discovery is used. Optional variables `NEBIUS_MODEL` and
`NEBIUS_BASE_URL` currently accept only the documented model/endpoint above.

After authorization and environment injection, run once:

```sh
python3 -B -m live_smoke --allow-paid-api --owner-authorization one-synthetic-request --account-cap-confirmed
```

This command has NOT been executed. It makes at most one inference request,
without retry, with a 15-second transport timeout and 256 output-token cap.
Redirects are refused. A timeout does not prove the provider did not bill the
request. CLI exits 0 on completed review, 1 on validation/provider failure, 2 on
usage errors. Live success requires both provider completion and a valid cited
selection; temperature zero does not guarantee deterministic inference.
Reasoning-only, truncated or non-JSON responses fail closed and may require
model-specific prompt/settings work after an authorized smoke test.

## Blockers and next steps

- Obtain authorization and credentials for one live smoke test; retain its
  allowlisted JSON with configured model, timestamp, source hash and numeric
  usage when available. Raw responses and sensitive headers are deliberately omitted.
- Export a small real simulation trace from the pinned core using its documented
  workflow outside this task; validate compatibility and data-use rights here.
- Extend the B2 frozen synthetic set with independently labeled real evidence.
  Run a separately authorized model-versus-baseline evaluation after the single
  smoke verification; no inference quality or latency measurements exist yet.
- Confirm Physical AI track fit and decide whether a future authorized simulation
  job on Nebius is needed. A mock-only evidence assistant is not prize-ready.
- Resolve this repository's missing open-source LICENSE and core/data provenance
  before distribution; no license was selected on the owner's behalf.
- Verify entrant registration/eligibility, prepare judging access, one-minute
  module demonstration within the short video, change disclosure and tool feedback.
  Distinguish the existing AegisLand system from the new Nebius contribution.

No deployment, paid request, push, merge or core modification was performed.
