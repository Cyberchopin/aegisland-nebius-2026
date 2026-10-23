# AegisLand — evidence review for Physical AI

Nebius × NVIDIA Global AI Hackathon 2026 submission repository.

**Real Nebius-hosted NVIDIA inference succeeded. Live citation-grounded review
remains `not_verified`.** This repository provides a working offline evidence
reader, deterministic review baseline, bounded provider adapter and preserved
runtime/failure evidence. Model recommendations cannot issue flight commands.

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

Do not rerun historical smoke commands or reset consumed guards. Do not use
`run_local_checks` with its default paths: it overwrites historical result JSON.
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
| Synthetic evaluation | No-model baseline 6/6; first-event mock 1/6 | Constructed harness results, not NVIDIA accuracy |
| B4 verification | 74 offline tests pass | No successful live review or model-quality benchmark |

Model: `nvidia/nemotron-3-super-120b-a12b`.
Successful runtime endpoint: `https://api.tokenfactory.nebius.com/v1/chat/completions`.
Usage-based cost estimates are not invoices or spending caps. All three allowances
are consumed. A fourth attempt has not been prepared or authorized.

NVIDIA documents non-thinking controls. Exact hosted Nebius support remains
unconfirmed; the new configuration is serialized/tested offline and fails
locally before transmission. No token-budget increase or speculative API retry
is enabled. Credentials remain environment-only and are never needed for the demo.

## Evidence and submission materials

- [Evidence table and artifact hashes](docs/submission/EVIDENCE_SUMMARY.md)
- [Recording runbook and narration](docs/submission/DEMO_SCRIPT.md)
- [Screenshot checklist](docs/submission/SCREENSHOTS_PLAN.md)
- [Devpost draft](docs/submission/DEVPOST_DRAFT.md)
- [Personal submission checklist](docs/submission/SUBMISSION_CHECKLIST.md)
- [Readiness](docs/NEBIUS_READINESS.md), [B4 research](docs/B4_REASONING_REMEDIATION.md),
  [trace contract](docs/TRACE_READER_CONTRACT.md), [evaluation contract](docs/MODEL_EVALUATION.md)

Video, screenshots and Devpost entry must be completed by the owner. Nothing
has been deployed, pushed, merged or submitted by this preparation work.

## Provenance and license

The separate [AegisLand core](https://github.com/Cyberchopin/aegisland-agentic-vision)
provides the prior simulation/perception work; the referenced baseline is
`eda23d3`. This competition repository does not import or copy core modules,
model weights or core video assets. Its new contribution is the trace-review
integration, synthetic evaluation, provider verification and failure diagnostics.
All local trace fixtures are synthetic; no real core trace regression, hardware
operation, flight certification, safety improvement or model speedup is claimed.

This integration is [MIT licensed](LICENSE). The license does not cover external
model/core/service rights. See [third-party boundaries](THIRD_PARTY_NOTICES.md)
and [license verification](docs/submission/LICENSE_VERIFICATION.md).
