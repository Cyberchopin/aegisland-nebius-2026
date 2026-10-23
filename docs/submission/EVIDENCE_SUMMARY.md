# Submission evidence table

**Real Nebius-hosted NVIDIA inference succeeded; live citation-grounded review
remains not_verified.** All three allowances are consumed. No fourth inference
candidate is prepared. Historical files are preserved, not regenerated.

| Evidence | HTTP | Returned model | Input / output tokens | Latency | Finish / review |
| --- | --- | --- | --- | --- | --- |
| `live_smoke.json` — 001 | 401 | Not returned | Not returned | 227.776 ms | Not retained / not_verified |
| `live_smoke_002.json` — 002 | 200 | Nemotron 3 Super | 324 / 256 | 2,304.33 ms | Not retained / not_verified |
| `live_smoke_003.json` — 003 | 200 | Nemotron 3 Super | 324 / 1,024 | 6,450.761 ms | length / not_verified |

Paths above are relative to `evaluation/results/`. Both successful inference
responses identify `nvidia/nemotron-3-super-120b-a12b` from the global Token
Factory chat-completions endpoint. Attempt 003 reported all 1,024 completion
tokens as reasoning and `failure_code: response_truncated`, confirming reasoning
budget exhaustion. Attempt 002 lacks the metadata needed to prove its cause.
Neither result records successful citation validation.

Estimated usage costs: 002 $0.0003276; 003 $0.0010188, at the rates recorded with
those requests. These are calculations, not invoices or hard account limits.
Single-request latency is not a benchmark. The records show technical runtime
integration, not overall contest eligibility or completed live-review functionality.

| Offline evidence | Result | What it establishes |
| --- | --- | --- |
| `evaluation/results/offline_evaluation.json` | Six synthetic scenarios: baseline 6/6, first-event mock 1/6 | Harness and mock behavior, not NVIDIA accuracy |
| `evaluation/b3/offline_tests.json` | 62 passing tests | Historical parser/diagnostic verification |
| `evaluation/attempt003_preparation/offline_tests.json` | 70 passing tests | Historical request-budget/guard isolation verification |
| `evaluation/b4/offline_tests.json` | 74 passing tests; 24 earlier artifacts unchanged | Current inference-code offline tests; hosted reasoning-control support remains unverified |

All trace fixtures are synthetic. No real core trace regression, external image
integrity validation, physical flight, safety gain or model-quality improvement
is claimed. The demo runbook generates new local displays and JSON outside the
repository; its mock/baseline output must retain those labels.

## Artifact identities

| Artifact | SHA-256 |
| --- | --- |
| `evaluation/results/live_smoke.json` | `b50107f155776362c51d32c3674633529a4c9cab9f2270e61a486b7dfba163d0` |
| `evaluation/results/live_smoke_002.json` | `399fe81ebe1a39a074359867f47ec17863d505da1cce320e0d6c9511944e1d36` |
| `evaluation/results/live_smoke_003.json` | `61805c7c375c0b2196cfaa07b94a5a6db14e51ba08fbcb3e89fa5150a10e2460` |
| `evaluation/results/live_attempt_consumed.json` | `143957b50213325dc33a0cfdc1c03ed6facec33a32e444f6a2992528b13de65f` |
| `evaluation/results/live_attempt_002_consumed.json` | `143957b50213325dc33a0cfdc1c03ed6facec33a32e444f6a2992528b13de65f` |
| `evaluation/results/live_attempt_003_consumed.json` | `143957b50213325dc33a0cfdc1c03ed6facec33a32e444f6a2992528b13de65f` |
| Fixed synthetic trace | `9ca93651e4a52ed889e3463c5a1ece3181e65a6656ebe0c9c2b6d21fcfa10b37` |

Identical guard hashes reflect identical contents, not a shared allowance.
Both earlier results and all consumed guards must remain present in the public
submission build. The complete preservation/test inventory is retained in B4
and the submission-preparation report; hashes establish file identity, not a
cryptographic attestation by Nebius.
