# B4 — reasoning-control compatibility

No live inference, guard resets, fourth request candidate, deployment, push or
merge. All 24 pre-existing evidence files, including three results and three
consumed guards, remain byte-for-byte unchanged. New B4 evidence lives in
`evaluation/b4/`; historical test JSON was not regenerated or overwritten.

## Confirmed failure

Attempt `b3-smoke-003` returned HTTP 200 in 6,450.761 ms. It reported 324 prompt
tokens, 1,024 completion tokens, and 1,024 reasoning tokens. `finish_reason` was
`length`; the safe failure code was `response_truncated`. The saved metadata
confirms that all of the completion allowance went to reasoning and generation
stopped at the limit. No successful review/citation was recorded. This is now
confirmed budget exhaustion, unlike the incomplete diagnostics from attempt 002.

## Primary-source research and compatibility boundary

[NVIDIA's Super model card](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16)
documents these OpenAI-client controls for its serving backends:

| Choice | SDK `extra_body` value | Decision |
| --- | --- | --- |
| Non-thinking | `{"chat_template_kwargs":{"enable_thinking":false}}` | Preferred model-level configuration |
| Low effort | `{"chat_template_kwargs":{"enable_thinking":true,"low_effort":true}}` | Model-level alternative; no strict small budget proven |

The same card's advanced budgeting example uses multiple calls, so it cannot be
substituted into this single-request workflow. `force_nonempty_content` is not
equivalent to disabling thinking; reclassifying reasoning as content would not
satisfy strict JSON/citation requirements. No sampling or input change is needed
to specify the preferred switch, so those are left unchanged.

[Nebius's Chat Completions reference](https://docs.tokenfactory.nebius.com/api-reference/inference/create-chat-completion)
documents the global URL and an extra-parameter mechanism, but does not confirm
`enable_thinking` or `low_effort` for this exact hosted Super ID. Its
[Super cookbook example](https://github.com/nebius/token-factory-cookbook/blob/main/models/nemotron/nemotron3-super-120B.md)
does not supply either control. Therefore model-level support is confirmed;
Nebius-specific compatibility is **not verified** from the reviewed primary
sources. SDK `extra_body` syntax is not proof that the hosted backend applies a
field. Other models' effort controls cannot establish support for Super.

With the OpenAI SDK the extra-body map is merged into request JSON; our direct
HTTP adapter's offline specification places `chat_template_kwargs` at the root,
not inside a literal SDK-style `extra_body` wrapper. This is the NVIDIA-shaped
serialization, not a claimed verified Nebius wire contract.

## Minimal implementation and safe failure

`NebiusProvider.build_request()` now provides a single tested serialization
path. Its default request is unchanged. The explicit offline configuration
`reasoning_mode="off"` serializes only the additional boolean setting above.
Unrecognized modes are rejected. No generic arbitrary-parameter passthrough,
environment switch, live CLI flag, fallback or retry was added.

Calling `complete()` in non-default mode fails locally with
`reasoning_configuration_unverified`, before any request attempt. This deliberate
gate remains until exact provider compatibility can be established. HTTP 400/422
also produce the redacted `provider_request_rejected` code without retry or
parameter removal. That code describes request rejection, not proof of which
field caused it. No HTTP 200 or serialized false flag is labeled as proof that
reasoning was disabled.

The fixed input, model ID, authentication, global endpoint, timeout, strict JSON
parser, citation validator and raw-output redaction remain intact. All historical
wrappers still encounter their consumed guards. Existing hosted settings and
output limits are unchanged; B4 does not increase the token allowance again.

## Verification and next prerequisite

**74 offline tests pass.** Added tests inspect the serialized request bytes,
verify root-level boolean `false` and unchanged messages/model/output limit,
verify local rejection before opening a connection, reject unsupported modes,
and exercise redacted HTTP 400/422 handling without retry. All HTTP responses
are synthetic; records and guards used by tests are temporary.

No independent attempt 004 is created because the provider-specific evidence
does not yet justify an executable candidate. Obtain a Nebius-owned documented
example, exported Playground configuration or provider confirmation for the
exact model and field placement. Then prepare a separately authorized bounded
test; first require normal final content, finish `stop`, and valid citations.
Reasoning counts must be recorded: positive counts would contradict an off-mode
claim; absent counts leave off-mode behavior unverified rather than proving zero.

Conditional cost planning only: if non-thinking mode is confirmed, use the
original 256 output-token cap. At the prior 324 input tokens, the recorded rates
give about **$0.0003276** at that cap; at an assumed 1,000 input tokens, about
**$0.0005304**. Prompt formatting may change counts. These are usage estimates,
not hard account limits, and no new paid request is authorized.

## Submission implication

Nebius-hosted NVIDIA runtime integration remains demonstrated. Live citation
grounding remains unverified. The demo and Devpost draft must show this boundary,
and may show deterministic synthetic baseline/mock operation as explicitly
offline footage. Finish licensing, real video/screenshots, judging instructions
and Devpost owner fields before October 30, 2026, 10:00 AM PDT. Avoid spending
the remaining schedule on unsupported parameters or larger blind token budgets.
