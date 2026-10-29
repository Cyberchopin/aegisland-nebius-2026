# Release status — PR #2 merged; updated October 29, 2026

## Saved local acceptance (October 27 snapshot)

- Saved CI-entry-point result: 83 tests passed locally on Windows, no failures/errors/skips.
  This is `verification/local_tests.json`, not the new Attempt 004 test run.
- Six unchanged trace/video artifacts match pinned upstream blobs. Three public
  provenance projections retain original identities and omit private metadata.
- Saved workbench check: all 230 stored event reviews were recomputed from
  original source lines and matched. New offline checks are retained separately.
- Rebuilding uses the pinned OpenCV snapshot; provenance output is an explicitly
  sanitized projection rather than a byte-for-byte copy of the source record.
- All 29 historical evaluation artifacts match the original Nebius archive.
- The Windows launcher changes to its own folder before starting the preview.
- Public demo files are bundled with the code; no API key or installation needed.

## Changes from the first submission-material package

The old CI runner blocked the loopback video test. It now permits exact 127.0.0.1
connections while still blocking external connections. CI uses a fresh `runs/`
directory, refuses existing/historical output paths and no longer overwrites
saved result JSON. Windows and Ubuntu hosted jobs completed successfully in
Tests run 40648963281.

## Publication status

PR #2 is merged. Current main is
`da0a2882b2126b4c67edb8b2329ce99b33075b50`.
[Tests run 40648963281](https://github.com/Cyberchopin/aegisland-nebius-2026/actions/runs/40648963281)
completed successfully on PR #2 head `4ce68b01799f58f23b2c6019b5bb2f26d0b95d6f`,
which is included in main. This is not a claim of a separate run on the merge SHA.
The acceptance JSON now distinguishes saved local evidence from verified remote
publication status. The updated video and Devpost text still require owner action.

The demo asset notice records original ownership boundaries. The owner must confirm
chosen public distribution terms and any collaborator rights for submitted media.
The updated recording still needs to be made and its actual URL entered on Devpost.

## Attempt 004 live review

Attempt 004 made exactly one bounded live request. Nebius returned HTTP 200 from
`nvidia/nemotron-3-super-120b-a12b`, with `finish_reason=stop`. Local citation
validation passed for source line 39 (`c71390b01d39`). Usage was 388 input and 40
output tokens; estimated cost was $0.0001524 at the recorded rates. See the
[minimal public verification summary](verification/attempt004_public_summary.json).

This is one limited live review, not evidence of model accuracy, real flight,
production safety or a long-term online service. The deterministic workbench
continues to review recorded simulation data. Hosted support for the requested
reasoning setting remains unconfirmed. Attempts 001–003 and their historical
evidence remain unchanged.

The OpenCV simulation, videos and traces are disclosed prior work. This revision
contributes the source-linked workbench, bounded review windows, citation
validation and Nebius model-review path. Attempt 004 used one request and no
retry. No deployment, video upload or Devpost update was made.

Historical documents under docs/submission/ describe earlier snapshots. Use the
root README and current submission/ copy for this candidate.
