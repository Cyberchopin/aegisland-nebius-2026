# AegisLand — evidence review for Physical AI

Nebius × NVIDIA Global AI Hackathon 2026 submission repository.

## New: source-linked simulation review workbench

The bundled workbench combines three existing OpenCV simulation replays with 230
validated original events, key-moment bookmarks, video frame seeking, source-line
inspection and downloadable deterministic review results. This is prior simulation
evidence connected to a new review interface, not fresh NVIDIA inference.

From this repository's folder, launch the demo with:

```sh
python -B scripts/serve_review_workbench.py --directory demo --port 8090
```

Open http://127.0.0.1:8090/ . On Windows, double-click `Start_Demo.cmd` to select
the correct working folder automatically. No API key or installation is required.
Video and traces are included in `demo/`; this is a local preview.

PR #2 is merged; published main is `da0a2882b2126b4c67edb8b2329ce99b33075b50`.
[GitHub Actions Tests run 40648963281](https://github.com/Cyberchopin/aegisland-nebius-2026/actions/runs/40648963281)
succeeded on PR #2 head `4ce68b01799f58f23b2c6019b5bb2f26d0b95d6f`, now included
in main. See [reuse, build instructions and next milestones](docs/REVIEW_WORKBENCH.md).
The builder verifies pinned source blobs and provenance hashes; no external core
code is copied or imported. Imported owner-provided media and records remain
in `demo/` and retain their original rights boundaries; the integration MIT
license does not grant a new license over those imported records or media.
Trace and video bytes are preserved. Provenance downloads are public summaries
with original source identities; private paths, commands and environment metadata
are omitted from those summaries.

**Attempt 004 completed one bounded live citation-grounded review.** The request
returned HTTP 200 from the configured model, finished with `stop`, and passed
local citation validation for line 39. This single review does not measure model
accuracy, establish real flight or production safety, or demonstrate a long-term
online service. See the [public verification summary](verification/attempt004_public_summary.json).
Model recommendations cannot issue flight commands.

## Run locally

Python 3.11+; standard library only. No installation, API key or paid service is
needed for these commands. Run from the repository root:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B -m trace_reader evaluation/traces/approval_conflict.jsonl
python3 -B -m nebius_review evaluation/traces/approval_conflict.jsonl
python3 -B scripts/demo_runbook.py --output-dir /tmp/aegisland-recording-01
```

The review command defaults to **SYNTHETIC / OFFLINE MOCK**, not NVIDIA inference.
The demo refuses an existing output directory; choose a fresh name on each run.
Add `--interactive` to pause between modules while recording. The runbook blocks
network/live provider calls, writes JSON plus `demo_report.html` outside this
repository, and checks historical evidence hashes before and after execution.
Open the generated HTML locally for screenshots; it is not a hosted application.

Do not rerun historical smoke commands or reset consumed guards. The current
check runner refuses existing output folders and protects historical evidence.
Use the same check entry point as CI:

```sh
python -B -m run_local_checks --output-dir runs/my-check-01
python -B scripts/check_workbench.py --directory demo
```

Choose a fresh results folder for each run. The check runner permits exact
127.0.0.1 connections for the video test and blocks external connections.
Windows and Ubuntu hosted CI completed successfully in the linked Tests run.
The saved 83-test result and 230-event recomputation remain historical release
evidence; new Attempt 004 preparation results are recorded separately.
Fresh offline evaluation can be written with:

```sh
python3 -B -m model_evaluation --output /tmp/nebius-offline-evaluation.json
```

## What the integration does

An explicit JSONL file is validated and hashed. A bounded projection contains
line/event identities, evidence risk values, approval metadata and reported
execution flags. The review interface accepts exactly one cited event and one
allowed check: `approval_gate` or `execution_claim`. Local code validates that
selection and evaluates the recorded facts. It does not infer physical execution
from a status flag or authorize a flight action.

The default mock selects the first event. The no-model baseline prioritizes
recorded approval conflicts, then execution reports. Both share strict parsing
and citation validation. Six synthetic scenarios compare them reproducibly.

## Retained results

| Source | Result | Limit |
| --- | --- | --- |
| Attempt 001 | HTTP 401; no returned model/usage | Authentication failed; precise cause unproven |
| Attempt 002 | HTTP 200, returned Nemotron 3 Super; 324 input / 256 output tokens; 2,304.33 ms | Review `not_verified`; old metadata cannot establish its exact failure |
| Attempt 003 | HTTP 200, returned same model; 324 input / 1,024 output tokens; 6,450.761 ms | All 1,024 output tokens were reasoning; finish `length`; review `not_verified` |
| Attempt 004 | HTTP 200; exact model; `stop`; line 39 citation passed; 388 input / 40 output tokens; estimated $0.0001524 | One bounded live review only; no accuracy, real-flight, production-safety or long-term-service claim |
| Synthetic evaluation | No-model baseline 6/6; first-event mock 1/6 | Constructed harness results, not NVIDIA accuracy |
| B4 verification | 74 offline tests pass | No successful live review or model-quality benchmark |
| Saved workbench release checks | 83 local tests passed; 230 stored reviews recomputed | Saved results, not model accuracy; PR #2 merged and hosted Tests run succeeded |

Model: `nvidia/nemotron-3-super-120b-a12b`.
Successful runtime endpoint: `https://api.tokenfactory.nebius.com/v1/chat/completions`.
The Attempt 004 cost is an estimate, not an invoice or spending cap. Attempts
001–003 remain unchanged. Attempt 004 made exactly one request; the service's
support for the requested reasoning setting remains unconfirmed.

NVIDIA documents non-thinking controls. Exact hosted Nebius support remains
unconfirmed; the successful response does not verify that the hosted service
honored the setting. No parameter-removal retry was made. Credentials are never
needed for the offline demo.

## Evidence and submission materials

- [Evidence table and artifact hashes](docs/submission/EVIDENCE_SUMMARY.md)
- [Current recording plan](submission/VIDEO_PLAN_EN.md)
- [Screenshot checklist](docs/submission/SCREENSHOTS_PLAN.md)
- [Current Devpost draft](submission/DEVPOST_COPY_EN.md)
- [Current release status](RELEASE_STATUS.md)
- [Readiness](docs/NEBIUS_READINESS.md), [B4 research](docs/B4_REASONING_REMEDIATION.md),
  [trace contract](docs/TRACE_READER_CONTRACT.md), [evaluation contract](docs/MODEL_EVALUATION.md)

A workbench screenshot is included at `docs/assets/workbench-preview.jpg`.
The updated video and Devpost entry still need owner completion. This branch
contains the published workbench; no deployment or Devpost update is implied. Historical
documents under `docs/submission/` describe the earlier evidence-only snapshot.

## Provenance and license

The separate [AegisLand core](https://github.com/Cyberchopin/aegisland-agentic-vision)
provides the prior simulation/perception work; the referenced baseline is
`eda23d3`. No core module or model weight is imported or copied. The `demo/`
folder bundles the owner's saved OpenCV simulation traces and display-video
derivatives with their upstream identities. They are disclosed prior work.
New contributions are the source-linked workbench, bounded review windows,
citation validation and Nebius model-review path, with synthetic evaluation and
provider/failure diagnostics.
All traces are synthetic simulation; hardware operation, flight certification,
safety improvement and model speedup are not established by this demo.

This integration is [MIT licensed](LICENSE). The license does not cover external
model/core/service rights. See [third-party boundaries](THIRD_PARTY_NOTICES.md)
and [license verification](docs/submission/LICENSE_VERIFICATION.md).
