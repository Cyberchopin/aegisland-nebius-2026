# Offline publication audit

Result: the local candidate is assembled and verified; nothing is staged or
committed by this audit. Source branch is `codex-b/stage-b1-nebius`, based on
`efd35cac2fbcfb8e24c0ef9d1112ae6688bfa328`. The cached main ref matches; remote
freshness is unknown because no network operation was performed.

## Scope and completeness

The exact [manifest](../evaluation/publication_audit/file_manifest.json) lists
66 candidate files and identifies the proposed 63-path change set. It includes
the provider adapter, evaluation/scenarios/tests, MIT license, README, notices,
demo runbook, Devpost/evidence/media instructions, all historical evidence and
three consumed guards. The index is empty; most implementation files remain
untracked until an authorized explicit staging operation.

A fresh temporary checkout assembled from the reviewed source manifest passed
**74 tests**. The recording command ran in that copy with network connections
blocked, produced all seven expected artifacts, and reported unchanged evidence
hashes. The outer network blocker observed zero connection attempts. The demo
also blocks the live provider directly and needs no credential. It is an offline
demonstration of modules and saved live results, not a replayed API request.

## Credential and account-data review

No credential-pattern findings were detected in the candidate or any of the four
existing commits. The index is empty; no credential/environment/cache path is
tracked or staged. Ignore checks pass for `.env`, `.env.local`, `.venv/` and
Python cache files. Current source includes intentional dummy credentials in
mock tests; those are not account keys.

Checks covered structured v1 tokens, private keys, AWS access-key IDs, GitHub and
other service tokens, long literal bearer values, labeled payment-card numbers,
sensitive JSON field names, and email addresses. No matches were found. All three
saved live results use allowlisted metadata fields and retain no raw answer,
reasoning text, auth header or raw request-ID field. Usage counts and hashed
provider request IDs remain. Pattern scanning and field inspection are bounded
checks, not a universal proof that arbitrary unknown secrets cannot exist.

## Accurate disclosure

The README, final Devpost draft, evidence table and recording instructions all
state that NVIDIA-hosted inference on Nebius succeeded while live citation
grounding is unverified. Attempt 001 is retained as HTTP 401. Attempt 002 is HTTP
200 without a verified review. Attempt 003 is HTTP 200 with finish `length` and
1,024 of 1,024 completion tokens reported as reasoning. No successful live review,
model accuracy gain, hardware flight or fourth inference is claimed.

Every one of the **27** pre-audit historical evidence files is unchanged,
including all three consumed guards and their request results. Existing audit
snapshots remain historical; new reports are separate. The user must record real
screenshots/video and complete personal Devpost fields; none are invented here.

## Publication caveats and owner gates

- **Commit blocker:** author and committer identities do not resolve in this
  execution environment. The owner must configure/select a public commit
  identity; this audit does not infer or expose an email address.
- CI runs `run_local_checks`, which regenerates `local_tests.json` and
  `offline_evaluation.json` in its isolated checkout before artifact upload. It
  does not rewrite Git history or consumed guards. Those regenerated copies
  should not be presented as immutable historical artifacts. A future CI output
  separation is optional maintenance, not a change made in this audit.
- Remote freshness, hosted CI success and GitHub MIT detection are unverified
  offline. Check them after an authorized publication.
- MIT is selected locally; the owner must confirm rights to contributions/media.
  Model/core/service rights remain separate.
- Live grounding remains incomplete. Further inference is blocked pending
  Nebius reasoning-control confirmation and new owner authorization.
- Actual media, eligibility/track fit, judging access and final Devpost submission
  remain owner tasks. Code publication alone does not complete the entry.

No local source-completeness or detected-secret blocker was found. Publication
still requires explicit owner approval. See [commit/PR plan](PUBLICATION_PLAN.md)
and [machine-readable checks](../evaluation/publication_audit/verification.json).
