# Live API verification gate

## B4 current state — three consumed allowances

Attempt 003 returned HTTP 200, finish `length`, and 1,024 reasoning tokens out of
1,024 completion tokens. All three results and consumed guards are preserved.
Do not run the historical commands below. B4 has 74 passing offline tests; all
24 prior evidence files are unchanged. No fourth attempt is prepared.
The non-thinking request specification is serialized and tested offline but
blocked with `reasoning_configuration_unverified` until exact hosted-provider
support is established. See [B4 remediation](B4_REASONING_REMEDIATION.md).
No new inference is authorized. All preparation/GO sections below are historical.

## Current state — attempt 003 candidate, execution NOT authorized

The owner authorized preparation of `b3-smoke-003` with a 1,024 output-token cap.
This is **not** final authorization to execute or an extension of either consumed
allowance. All 20 prior evidence files are unchanged, including both consumed
guards. 70 offline tests pass; zero live requests were made in preparation.
Previous status sections below are historical.

Candidate command for the owner's local WSL terminal, **only after separate GO**:

```sh
NEBIUS_BASE_URL=https://api.tokenfactory.nebius.com/v1 python3 -B -m live_smoke_third --allow-paid-api --owner-authorization one-synthetic-request --owner-accepts-no-account-cap
```

It saves sanitized JSON exclusively to `evaluation/results/live_smoke_003.json`
and claims only `evaluation/results/live_attempt_003_consumed.json`. Neither
file exists yet. No stdout redirection is needed. Existing evidence destinations
are never overwritten. After an attempted failure, stop; no retry or guard reset.

The model, fixed input messages, temperature zero, global endpoint, 15-second
socket timeout, no retries, redirect refusal and diagnostics are unchanged.
Only `max_tokens` changes, from 256 to 1,024, for this candidate. The provider
default and prior attempt wrappers remain at 256. No reasoning-disable setting
or new interpretation of citations has been added. A larger allowance may still
be insufficient; finish reason and safe failure codes remain authoritative.

At the previously observed 324 prompt tokens and the full 1,024 output cap,
estimated usage cost at the recorded rates is $0.0010188. A planning estimate
with 1,000 prompt tokens is $0.0012216. Exact input count, model accounting and
current invoice rates must be checked when executing. These are estimates, not
a guaranteed maximum bill or a hard account-side cap. No top-up or compute is
provisioned. The owner must explicitly extend acceptance of absent account-side
limits and possible payment-card charges to this third request.

Required authorization, after private credential configuration:

> FINAL GO for b3-smoke-003: authorize exactly one potentially billable synthetic
> request with 1,024 maximum output tokens, the fixed model/input/global endpoint,
> 15-second timeout and zero retries. Accept no verified account-side spending
> cap and possible linked-card charges for this request only. Preserve all prior
> records and stop after the attempt, without retry.

Candidate manifest and offline regression results are in
`evaluation/attempt003_preparation/`. Synthetic tests cover payload equivalence
apart from output cap, limit validation, previous guard/evidence isolation,
exclusive evidence creation, consumed-third-guard refusal, redaction, safe
truncation diagnostics and timeout without retry. Both existing guards remain
consumed and are not bypassed by their original commands.

## B3 current state — both allowances consumed

The owner executed attempts 001 and 002 locally. Attempt 001 returned HTTP 401;
attempt 002 returned HTTP 200 and the expected NVIDIA model, but the review was
`not_verified`. **Both guards are consumed. Do not run the historical commands
below, reset guards or create a third attempt without new authorization.**
B3 is offline only: 62 tests passed, existing evidence unchanged, no inference.
Future diagnostics now retain allowlisted finish reasons, numeric token details
and safe validation failure codes, never raw model text. See
[B3_FAILURE_ANALYSIS.md](B3_FAILURE_ANALYSIS.md). Any suggested increase in output
tokens is a proposal, not an implemented or authorized third request.

The preparation and authorization sections below are historical records.

## Current state — second attempt prepared, final authorization pending

The owner ran attempt 001 locally: HTTP 401, 227.776 ms, no returned model or
usage, no citation validation. Its allowance is consumed. Preserve permanently:
`evaluation/results/live_smoke.json` and
`evaluation/results/live_attempt_consumed.json`. Preparation verified their
SHA-256 values unchanged; see `evaluation/results/second_attempt_preparation.json`.
Earlier unconsumed/awaiting-first-GO statements below are historical.

Endpoint review: the [official quickstart](https://docs.tokenfactory.nebius.com/quickstart)
uses `https://api.tokenfactory.nebius.com/v1/` and the chat-completions path.
[Public endpoint documentation](https://docs.tokenfactory.nebius.com/public-serverless)
warns that regional URLs can stop working as processing locations change.
The [Nemotron example](https://nebius.com/services/token-factory/nemotron) also
documents us-central1; the original selection was therefore sourced, but its
account/model suitability is not established. Attempt 002 deliberately selects
the quickstart's global URL for public inference. This is not proof that region
mismatch caused the 401 or that the new key has been authenticated.

Independent identifier: `b2-smoke-002`. New exclusive guard:
`evaluation/results/live_attempt_002_consumed.json`. New evidence destination:
`evaluation/results/live_smoke_002.json`. Neither exists yet. The second command
creates its evidence destination exclusively and refuses existing evidence;
never redirect its output to the first attempt's files. The original command
continues to be blocked by its original consumed guard.

**Preparation only is authorized. Wait for the owner's separate final GO.**
After final GO, run from this repository in the local WSL shell holding the key:

```sh
NEBIUS_BASE_URL=https://api.tokenfactory.nebius.com/v1 python3 -B -m live_smoke_second --allow-paid-api --owner-authorization one-synthetic-request --owner-accepts-no-account-cap
```

The command saves sanitized JSON to its own destination and prints the same
record. A conflicting endpoint environment override is rejected, with no
automatic regional fallback. Model, fixed payload, 256 output-token limit,
15-second timeout and zero retries are unchanged. Payload SHA-256 remains
`e34d598f35ddd27392d8cb0c3126eba41616c0594d5e4297c1bb3087395ae718`.
The no-account-cap flag records risk acceptance, never asserts a spending cap.
On attempted failure, do not retry or reset either guard.

55 offline tests pass, including consumed-first/independent-second isolation,
identical payload, global endpoint, unchanged limits, second-guard refusal,
existing-evidence refusal, timeout, and missing authorization. HTTP is mocked;
tests use temporary records. No live inference occurred during preparation.

## Current owner authorization — awaiting final GO

The owner approved `--owner-accepts-no-account-cap` for exactly one fixed
synthetic Nemotron request, explicitly accepting that promotional credits are
not a spending cap and a saved payment card may be charged. This flag is
mutually exclusive with `--account-cap-confirmed`; output records the chosen
`billing_authorization` without asserting an account-side cap for the new mode.
Earlier hard-cap requirements below are historical for this one-request exception.

Implementation and offline tests only are currently authorized. **Do not execute
until the key is privately configured and the owner separately gives final GO.**
47 offline tests pass; the original payload hash is unchanged:
`e34d598f35ddd27392d8cb0c3126eba41616c0594d5e4297c1bb3087395ae718`.
The persistent guard remains unused and unchanged. No live request was made.

After final GO, exactly once:

```sh
python3 -B -m live_smoke --allow-paid-api --owner-authorization one-synthetic-request --owner-accepts-no-account-cap > evaluation/results/live_smoke.json
```

Model, fixed input, 256 output-token limit, 15-second timeout, no retries and
exclusive persistent attempt claim are unchanged. Failure consumes the allowance;
do not reset the record or retry without new owner authorization.

**Disabled by default. Conditional owner authorization received 2026-10-22;
no live request performed.** Exactly one attempted inference is authorized,
using only the fixed synthetic fixture, without retries, subject to privately
configured credentials and a verified total billable ceiling of $1. If the cost
cannot be bounded or checked beforehand, stop and request owner approval.
This authorization has not been consumed. A CLI flag does not enforce a dollar
ceiling, and the existing estimated cost is not sufficient to establish one.

The current offline preflight finds no `NEBIUS_API_KEY`; account access and the
cost ceiling remain unverified. Gate evidence is preserved in
`evaluation/results/live_verification_gate.json`. No attempt, actual model,
latency, usage, or actual cost is claimed. The local-only readiness fix now
records response-model identity, HTTP status, elapsed latency, usage and estimated
cost. A verified account-side spending cap remains required; the confirmation
flag is an owner attestation, not a spending control.

Final local evidence: 44 tests pass and all code-level preflight checks pass.
Output is capped at 256 tokens, transport timeout at 15 seconds. The fixed input
has 1,069 content characters (roughly 267 tokens by characters/4; exact model
tokenization and chat overhead are unverified). `max_tokens` uses the existing
OpenAI-compatible API parameter. Reasoning may exhaust the 256-token allowance;
truncation fails validation without retry or automatic token-limit increases.
No additional preflight audits are needed unless code or configuration changes.

The provider permits only one attempt per instance. An exclusive persistent
`evaluation/results/live_attempt_consumed.json` claim also prevents command
reruns and concurrent attempts. Do not delete or reset this record without new
owner authorization. No record is claimed during preflight or missing-credential
failure. Tests use isolated temporary paths and mocked transport.

## Exact route and prerequisites

- Method: `POST`.
- URL: `https://api.tokenfactory.us-central1.nebius.com/v1/chat/completions`.
- Model: `nvidia/nemotron-3-super-120b-a12b`.
- Credential: environment variable `NEBIUS_API_KEY`, sent as bearer auth.
- Optional `NEBIUS_BASE_URL` and `NEBIUS_MODEL` must match the B1 allowlist;
  no automatic region/model fallback or redirect is permitted.

[Nebius's example](https://nebius.com/services/token-factory/nemotron) documents
this regional base URL and model ID (rechecked 2026-10-21). Account-specific
availability has not been verified. The owner needs a Token Factory account,
accepted service/model terms, a valid scoped API key, model/region access,
sufficient quota or credits, and HTTPS network access. An AI Cloud credential
should not be assumed interchangeable with a Token Factory key.

## Minimum owner actions

Check local prerequisites without authorization or network access:

```sh
python3 -B -m live_smoke --preflight
```

This checks the fixed trace and credential/configuration presence, without
printing their values. Exit 1 means local prerequisites are missing; exit 0
means they are present. Even with both live flags, preflight never calls the
API; account access, quota and pricing remain unverified. The 2026-10-22 result
is retained in `evaluation/results/offline_preflight.json`: trace valid,
credential/configuration unavailable, zero live calls.

1. Authorize **one potentially billable inference request** using the fixed
   synthetic approval-conflict trace, including upload of its projected evidence.
2. Inject `NEBIUS_API_KEY` into the execution environment through a secret manager
   or private shell. Do not paste the value into chat, source, command arguments
   or shell history. Confirm account access, quota and pricing in the console.
3. After authorization, execute (or instruct Codex to execute) this exact command:

```sh
python3 -B -m live_smoke --allow-paid-api --owner-authorization one-synthetic-request --account-cap-confirmed
```

No output-path flag is needed: stdout is one sanitized JSON record suitable for
retention in `evaluation/results/live_smoke.json` by shell redirection after
authorization. Running without both flags emits `status: disabled`, exits 2,
and does not construct a provider. The flags express the operator's attestation;
they are not an authorization service and must not be supplied autonomously.
The B1 live CLI remains subject to the same owner-authorization requirement.

## Cost controls and estimate

Exactly one completion attempt, no retry, temperature zero, `max_tokens: 256`,
non-streaming, 15-second socket timeout, 256-KiB response limit. The fixed
two-event synthetic trace is bounded by the adapter's 32-event/32-KiB packet
limits. No deployment, polling, model discovery or follow-up inference occurs.
A timeout may still be billed and is not permission to retry. The socket timeout
is not a strict total wall-clock deadline.

[Nebius's public model page](https://nebius.com/services/token-factory/models/nvidia-nemotron-models-inference)
lists Super at $0.30/million input tokens and $0.90/million output tokens
(checked 2026-10-21). At an **assumed** 2,000 input tokens and the 256 output cap,
arithmetic is $0.0006 + $0.0002304 = **$0.0008304**, before taxes or other charges.
This is an estimate, not a metered measurement or guaranteed spending ceiling.
There is no local tokenizer or enforced dollar budget; reasoning-token accounting,
service terms and current console prices must be checked. Use account-side
limits where available. Request-size limits do not alone enforce a token budget.

## Success and safe failure

Exit 0 / `status: verified` requires a completed response (`finish_reason: stop`),
no explicit refusal, strict JSON with exactly the allowed selection fields,
a supported check, and a citation matching the submitted event. The JSON
separately records `matches_synthetic_expectation`: expected line 2, evidence
`synthetic-approval_conflict-1`, `approval_gate`, and recorded approval conflict.
Protocol verification can succeed while this quality condition is false; report
that as a fixture-quality failure, never an accuracy improvement.

Errors/refusal/invalid JSON/invalid citation/timeout exit 1 with
`status: not_verified` and a generic reason. Missing credentials set
`request_attempted: false`. An attempted request does not prove provider receipt
or billing. There is no baseline fallback in this command. Mocked smoke tests
exercise this path but are not retained as live verification.

The output allowlist includes local timestamp, configured model/endpoint, source
SHA-256 on success, booleans and validated integer usage counts if supplied.
It discards raw response content, refusal text, request/response headers,
authorization tokens, cookies, raw provider IDs, arbitrary metadata and exception
text. Usage counts are counts, not raw token text. No HTTP debug logging is
enabled. Do not enable external HTTP tracing, dump environment variables or use
shell tracing during verification. This is application output redaction, not a
guarantee about unrelated host instrumentation.

The response's model must exactly match the configured allowlisted NVIDIA ID
before `verified` is emitted. Unknown names are redacted and fail verification.
The provider request ID is retained only as SHA-256, from `x-request-id` or the
response JSON `id`; no arbitrary header is logged. Numeric usage metadata and
elapsed latency are retained even for a parsed refusal/truncation where available.
Estimated cost uses actual prompt/completion counts at the published rates above;
missing counts yield null. It is not the final invoice or an enforceable cap.

A single successful call establishes protocol compatibility only. It does not
establish real-trace performance, flight safety, track eligibility or prize
readiness. Model recommendations remain outside the command execution path.
