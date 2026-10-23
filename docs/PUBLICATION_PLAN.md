# Proposed commit and draft PR — not executed

Branch: `codex-b/stage-b1-nebius`.
Current HEAD and cached `origin/main`: `efd35cac2fbcfb8e24c0ef9d1112ae6688bfa328`.
Remote freshness has not been checked during this offline audit.
The index is empty. No new commit, stage operation, fetch, push or PR was made.
Git author and committer identities do not currently resolve in this execution
environment. Before committing, the owner must configure the intended public
name/email (a GitHub noreply address is an option) or provide them separately.
They are not stored in these audit documents. Do not invent an author identity.

## Exact content

Use [file_manifest.json](../evaluation/publication_audit/file_manifest.json) as
the allowlist. It specifies the complete 66-file candidate tree: 61 new files,
2 modified files, and 3 existing unchanged files. The proposed commit changes
63 paths. It includes the MIT license, README, original integration/tests,
synthetic fixtures, all 27 historical evidence files, three consumed guards,
offline demo script, submission materials and four publication-audit artifacts.
No ignored environment files, caches or local virtual environment are included.

The manifest and verification report cannot contain their own final content
hashes; these two entries explicitly record that exclusion. Other entries carry
SHA-256 hashes and modes. Recheck hashes and the exact path list before staging.
Do not use a blanket `git add .` or include extra files after owner approval.

## One proposed commit

Title: `Prepare AegisLand Nebius submission with preserved runtime evidence`

Include the 63 changed paths in the manifest in one reviewed commit, retaining
the three unchanged baseline files through normal Git ancestry. This is a
single competition-integration delivery, including B1–B4 work and submission
preparation. Do not amend the four baseline commits or rewrite their history.
A new commit SHA does not exist yet and must be recorded after creation.

After authorization:

1. Confirm HEAD, branch, file hashes and index still match the audited state.
   Confirm the owner-selected public author/committer identity resolves.
2. Refresh remote refs without force; if remote/base changes create a material
   difference, report it before publishing an altered change set.
3. Stage only manifest entries marked `added` or `modified`; verify cached diff,
   credential scan and all three guard/result hashes. Commit using the title above.
4. Push the new commit to `origin/codex-b/stage-b1-nebius`, without force.
5. Open a **draft PR** against `main` with the description below. Report the
   actual commit SHA and PR URL. Stop without merging or deploying.

No API key, account configuration, model inference, video upload or Devpost
submission is part of this Git publication authorization.

## Draft PR content

Title: `Prepare AegisLand Nebius submission and retain live verification limits`

Description:

> Adds a bounded trace-review adapter and reproducible synthetic comparison with
> a deterministic baseline. Real owner-run requests reached NVIDIA Nemotron 3
> Super on Nebius Token Factory, while live citation-grounded review remained
> `not_verified`. Attempt 003 confirms reasoning-budget exhaustion; the proposed
> non-thinking configuration fails locally until hosted compatibility is confirmed.
>
> Preserves all three results and consumed guards. Adds MIT licensing with
> external-rights boundaries, an offline recording runbook, and submission copy
> that discloses the failed review. The review path cannot issue hardware commands.
>
> Validation: 74 tests pass in a fresh candidate assembled from the manifest;
> the demo succeeds with network blocked and zero provider calls. The offline
> audit found no credential patterns in candidate content or the four baseline
> commits. Historical hashes are unchanged. See `docs/PUBLICATION_AUDIT.md`.
>
> Remaining release work: owner-recorded video/screenshots, personal Devpost
> fields, rights/eligibility confirmation and verification of the published
> checkout. CI regenerates two offline report files in its checkout; use committed
> historical evidence rather than those regenerated artifact copies for provenance.

## Required owner authorization

> I authorize staging and creating the single commit described in
> docs/PUBLICATION_PLAN.md from the audited manifest, pushing it without force to
> origin/codex-b/stage-b1-nebius, and opening a draft PR against main. Preserve
> every historical result and consumed guard. Do not merge, deploy, submit
> Devpost, upload media, change inference settings or make any API calls. Stop
> and report the actual commit SHA and PR URL.

The owner must also confirm the public Git identity to use, or configure it
before the authorized operation. That identity will be visible in the commit.

If the owner wants a local commit only, omit the push/PR authorization explicitly.
