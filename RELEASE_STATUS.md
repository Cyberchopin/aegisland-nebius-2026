# Release candidate v2 — October 27, 2026

## Local acceptance

- CI entry point: 83 tests pass locally on Windows, no failures/errors/skips.
- Six unchanged trace/video artifacts match pinned upstream blobs. Three public
  provenance projections retain original identities and omit private metadata.
- All 230 stored event reviews recomputed from original source lines and matched.
- Rebuilding uses the pinned OpenCV snapshot; provenance output is an explicitly
  sanitized projection rather than a byte-for-byte copy of the source record.
- All 29 historical evaluation artifacts match the original Nebius archive.
- The Windows launcher changes to its own folder before starting the preview.
- Public demo files are bundled with the code; no API key or installation needed.

## Changes from the first submission-material package

The old CI runner blocked the loopback video test. It now permits exact 127.0.0.1
connections while still blocking external connections. CI uses a fresh `runs/`
directory, refuses existing/historical output paths and no longer overwrites
saved result JSON. Windows and Ubuntu jobs are configured; hosted runs are pending.

## Publication status

This release is prepared for review on branch `codex/review-workbench-v2` of
Cyberchopin/aegisland-nebius-2026, based on main at `508238f`. The JSON acceptance
record is a local pre-publication snapshot; see GitHub for current branch and CI
status. No merge or Devpost update is implied by publication of this branch.
Wait for actual hosted CI before merging. Local Windows checks do not establish
a passing Ubuntu hosted run.

The demo asset notice records original ownership boundaries. Confirm the owner's
chosen public distribution terms and any collaborator rights before publication.
The updated recording still needs to be made and its actual URL entered on Devpost.

## Model milestone remains open

Successful live citation-grounded Nemotron review is not_verified. The workbench
shows deterministic checks over saved simulation data. Do not claim model-quality
gains, autonomous physical flight or new hardware validation. No paid request or
deployment was made during acceptance.

Historical documents under docs/submission/ describe earlier snapshots. Use the
root README and current submission/ copy for this candidate.
