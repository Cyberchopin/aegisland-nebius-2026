# Devpost submission text

Technical copy is ready for owner review. Fill the personal fields and final URLs
at the end before submitting. Evidence cutoff: B4; no fourth inference occurred.

## Project name

AegisLand — evidence review for Physical AI

## Short description

Review synthetic Physical AI traces with a deterministic baseline and NVIDIA
Nemotron on Nebius. Real inference works; live citation grounding is still
unverified. Model output cannot issue flight commands.

## Inspiration

A simulation's decision, approval state and execution flag can tell different
stories. An operator needs to inspect the recorded evidence without treating a
status flag as proof that hardware moved. This project applies that distinction
to AegisLand's simulation traces.

## What it does

An explicit JSONL trace is validated and hashed. The review interface receives a
bounded evidence packet and may select only a source line, its evidence ID and
one of two allowed checks. Local code rejects malformed JSON, unsupported checks
and unmatched citations before evaluating recorded approval/execution consistency.
The review path has no hardware adapter or authority to issue flight commands.

The offline demo shows a deterministic baseline finding an approval conflict and
a labeled mock missing that target. Six constructed scenarios make the comparison
reproducible. Baseline 6/6 and mock 1/6 are harness results, not NVIDIA model scores.

## How we built it

Python's standard library handles trace validation, SHA-256 provenance, HTTP
integration and tests. The hosted model is `nvidia/nemotron-3-super-120b-a12b`,
served through `https://api.tokenfactory.nebius.com/v1/chat/completions`.
Credentials stay in the environment. Each authorized smoke allowance has its own
persistent guard, no retries and sanitized evidence. The demo itself is offline
and reads saved real results rather than rerunning inference.

The AegisLand core is prior work, referenced at `eda23d3`; no core module or model
weight is imported/copied here. The competition-specific contribution is the
trace reader, bounded review interface, synthetic baseline evaluation, guarded
NVIDIA/Nebius runtime integration and failure diagnostics. The integration
repository is MIT licensed; external model and service rights remain separate.

## What we verified

Real Nebius-hosted NVIDIA inference succeeded. Attempt 002 returned HTTP 200 and
the expected model, used 324 input/256 output tokens, and took 2,304.33 ms. Its
review was `not_verified`; the original diagnostics cannot establish its exact
failure. Attempt 003 also returned HTTP 200, used 324 input/1,024 output tokens,
and took 6,450.761 ms. All 1,024 output tokens were reported as reasoning;
`finish_reason` was `length`, and the review remained `not_verified`.

These are individual recorded requests, not latency benchmarks. Estimated usage
costs were $0.0003276 and $0.0010188 at the recorded rates, not invoices or hard
spending caps. We retain the failed first attempt (HTTP 401) as well.

B4 has 74 passing offline tests covering parsing, citations, transport failures,
redaction and request isolation. NVIDIA documents a non-thinking setting, but
Nebius-specific support for the exact hosted model is unconfirmed. Its offline
serialization is tested and blocked from transmission. There is no fourth
attempt and no successful live citation result to claim.

## Challenges and lessons

The first request failed authentication; the precise cause is not established.
The global endpoint and a later key reached the model, but inference success did
not mean a usable review. Increasing the output allowance to 1,024 exposed a
reasoning-budget problem rather than resolving it. We added allowlisted finish
reasons, numeric token details and safe failure codes without retaining raw
reasoning or answers. Strict citation checks remain in place.

## Next steps

Obtain provider confirmation of non-thinking support before any new authorized
request. Then evaluate independently labeled real simulation traces against the
baseline. We have not demonstrated real-trace quality gains, autonomous flight,
hardware operation, physical safety improvement or a model performance advantage.

## Built with

Python, Nebius Token Factory, NVIDIA Nemotron 3 Super, JSONL, unittest, GitHub
Actions. AegisLand simulation/perception is referenced prior work, not reproduced
by the current integration's synthetic test evidence.

## Tool feedback

The global Token Factory endpoint returned the expected model and usage metadata.
The 1,024-token run's finish reason and reasoning-token counts made its failure
diagnosable. Clear hosted-model documentation for thinking controls would help
small bounded extraction tasks avoid spending the whole allowance on reasoning.
No service-side reasoning switch is claimed to work here.

## Owner fields to complete

- Proposed track: **Physical AI**; personally confirm fit for these simulation/evidence modules.
- Public source: `https://github.com/Cyberchopin/aegisland-nebius-2026`; verify the final reviewed code and MIT license are actually published there.
- Video URL: **[paste the actual public YouTube URL]**.
- Screenshots: **[attach actual captures and the prepared captions]**.
- Judging instructions: use the offline commands in README and `scripts/demo_runbook.py`; disclose that another live call is blocked pending provider support and owner authorization.
- Team/representative: **[enter legal/account details privately in Devpost]**.
- Significant-update statement: **[confirm contribution dates within the submission period and ownership of the new work described above]**.
- AI assistance: Codex assisted implementation, tests, analysis and submission copy; the owner reviewed claims and separately authorized each paid request. **[confirm accuracy and satisfy any current form disclosure field]**.
