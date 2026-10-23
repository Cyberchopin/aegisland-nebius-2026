# B3 — offline failure analysis

No network requests, third attempt or guard resets. Existing evidence was
snapshotted before changes: every one of the 11 files in `evaluation/results/`
remains byte-for-byte unchanged. B3 artifacts are stored separately under
`evaluation/b3/`. Both consumed guards remain in place.

## Confirmed facts

Attempt 001 returned HTTP 401. Attempt `b2-smoke-002` reached the global Nebius
Token Factory endpoint, returned HTTP 200 and model
`nvidia/nemotron-3-super-120b-a12b`, elapsed 2,304.33 ms, and reported 324 prompt
tokens, 256 completion tokens and 580 total tokens. Its estimated cost was
$0.0003276 at the recorded published rates; this is not an invoice.

This demonstrates real Nebius-hosted NVIDIA inference. The review result is
`not_verified`: no successful citation or expected-selection check was recorded.
There is no retained raw model text, finish reason or reasoning-token breakdown.
The output used the entire configured 256-token allowance. This is strong
motivation to investigate the budget, but is not proof of truncation.

## Request and failure path

- Request: OpenAI-compatible `POST /v1/chat/completions`, two text messages,
  temperature 0, `max_tokens: 256`, `stream: false`, fixed two-event synthetic
  projection. No `response_format`, tools, explicit reasoning controls or chat
  template settings are supplied. The service's reasoning default is unknown.
- Transport: one completion call, 15-second socket timeout, no application/SDK
  retry, no redirects, capped response bytes. The socket timeout is not a total
  wall-clock deadline.
- Envelope: model and usage are captured before content validation. A refusal
  or any finish reason other than `stop` rejects the result, even if returned
  text happens to look like complete JSON.
- Parser: strict JSON only; duplicate keys, nonfinite constants, partial JSON,
  empty text, prose, code fences or reasoning mixed into content are rejected.
- Selection: exactly `line`, `evidence_id`, `check`; line must be an integer,
  evidence ID a string, and check one of `approval_gate` or `execution_claim`.
  Both the physical source line and evidence ID must match one supplied event.
  The local finding evaluator then checks the selected recorded evidence.
- Runtime identity: the returned model must exactly equal the configured ID.
  The saved second response already matches it, so that specific mismatch is
  not a leading explanation for attempt 002.

The old generic failure reason collapsed envelope, parse, schema and citation
failures. Thus `finish_reason: length`, reasoning consuming most/all output,
malformed selection JSON, unsupported fields/checks, wrong citation or refusal
remain hypotheses. We cannot reconstruct the actual answer, identify the failed
stage, or retroactively validate citations from the retained metadata.

## Diagnostics implemented, without changing inference settings

`finish_reason` is now retained before refusal/content validation using an
allowlist (`stop`, `length`, `content_filter`, `tool_calls`, `function_call`).
Unknown values become `unrecognized`; absent fields remain null. Numeric
`prompt_tokens_details` and `completion_tokens_details` are projected through
explicit key/type/range checks, including reasoning and cached token counts when
the service supplies them. Missing details remain missing, never synthesized.

Safe failure codes distinguish `response_truncated` (only provider `length`),
`response_not_complete`, `model_refusal`, `invalid_provider_response`,
`missing_content`, `invalid_selection_json`, `missing_citation`,
`invalid_selection_schema`, `unsupported_check`, `citation_mismatch` and
`response_model_mismatch`. Unknown codes become `review_failed`.
No exception text, raw model answer, reasoning text, credential, or arbitrary
metadata is retained. Existing HTTP/model/usage/latency/hashed-request-ID
redaction is preserved. New diagnostics cannot backfill attempt 002.

## Smallest justified next change — proposal only

For a separately authorized future request, increase only `max_tokens` from 256
to **1,024**, leaving the fixed prompt, model, timeout, no-retry policy and strict
citation validator unchanged. This provides reasoning/answer headroom and avoids
an unverified provider-specific reasoning-disable flag. At the previous 324
input tokens and 1,024 output tokens, arithmetic at the recorded rates would
be approximately $0.0010188; actual input, billing and reasoning accounting may
differ. This is not a spending cap or a guarantee of sufficient answer budget.

**Not implemented or authorized for execution.** The current limit is still 256.
No third identifier, evidence destination or request allowance was created.
A future request would need explicit owner authorization and a new independent
guard; neither consumed guard may be reused. Its finish reason and safe failure
code would distinguish output-budget exhaustion from parser/citation failures.
Do not weaken citation checks or strip arbitrary prose to manufacture success.

## Offline verification

62 tests pass, zero failures/errors/skips. The 11-case synthetic parser fixture
includes valid/missing/invented/wrong-line citations, unsupported checks, partial
and malformed JSON, empty content, code fences, duplicate keys and extra fields.
Mocked HTTP tests distinguish `length` even with valid-looking JSON, preserve
refusal metadata, redact unknown finish reasons and reject sensitive/invalid
token-detail values. Test guards are temporary files, never real attempt guards.

Evidence: `evaluation/b3/offline_tests.json` contains code hashes, test results
and the preserved evidence hashes; `evaluation/b3/failure_analysis.json` records
confirmed facts separately from hypotheses. B3 did not run `run_local_checks`
because that command overwrites historical B2 test/evaluation JSON. Historical
results remain preserved. The new tests are discovered by the existing CI.
