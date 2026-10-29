# Review workbench — release status updated October 29, 2026

## Public provenance update

Published provenance is an allowlisted summary containing source revision,
original source hashes, core pin, validation counts and trace identity. Home
paths, commands and environment overrides from original run metadata are omitted.
Six trace/video files retain exact upstream bytes; three provenance summaries
are labeled projections. The saved workbench snapshot includes 83 local tests;
new Attempt 004 regression results are retained separately.

## Published release

PR #2 is merged; main is `da0a2882b2126b4c67edb8b2329ce99b33075b50`.
[Hosted Tests run 40648963281](https://github.com/Cyberchopin/aegisland-nebius-2026/actions/runs/40648963281)
succeeded on PR #2 head `4ce68b01799f58f23b2c6019b5bb2f26d0b95d6f`, included
in that merge. The 83 local tests and 230-event recomputation are saved release
results, not newly generated model evaluations. Six original trace/video artifacts
match upstream bytes; the three provenance summaries are sanitized projections.
The new video and Devpost update remain owner tasks.

## What is implemented

Three existing recorded OpenCV simulation scenarios feed a new source-linked
review interface. All 60 nominal, 90 intrusion and 80 GPS/low-light events pass
the existing trace contract. Imported traces remain byte-for-byte original.
Each selected event shows the recorded action/reasons, approval state, execution
flags, motion risk, active-perception flag and a deterministic single-line check.
The same line/evidence ID and full trace SHA-256 accompany JSON exports.

Bookmarks are curated, not a model or baseline quality benchmark. The prior
6-scenario synthetic comparison remains separate and unchanged. The full core
test suite and OpenCV inference are not rerun by this workbench.

`review(path, provider, line_window=(first, last))` validates the whole source
trace before projecting at most 32 original source lines. Existing behavior
without a window remains bounded to 32 events. Responses citing an event outside
the supplied window are rejected; original full-file hashes and line numbers
survive. The review packet remains bounded to 32 KiB. This feature does not
grant permission to transmit traces or call paid services.

## Reproduce

Use Python 3.11+ and an unmodified source snapshot of
`Cyberchopin/aegisland-opencv-2026` at
`de93d5a25de42f00546a62c9e728ee1d8da6c5b6`.
No packages or API credentials are required. From the Nebius repository:

```powershell
python -B scripts/build_review_workbench.py --source PATH_TO_OPENCV_SOURCE --output PATH_TO_NEW_OUTPUT
python -B scripts/serve_review_workbench.py --directory PATH_TO_NEW_OUTPUT --port 8088
```

Open `http://127.0.0.1:8088/`. The server binds only to loopback and supports
video byte ranges for frame seeking. Stop with Ctrl+C. Double-clicking index.html
can also display the workbench; seeking behavior depends on the local browser.
No hosted demo or currently running cloud backend is implied.

The source pin verifies exact Git blob identities for all copied inputs and the
media manifest before building. Trace SHA-256 values must also match original
provenance; H.264 derivatives must match the source media manifest. A fresh
output directory is mandatory. No historical evaluation artifact is overwritten.

## Reuse map

| Source | Reuse in this iteration | Boundary |
| --- | --- | --- |
| OpenCV repository, pinned above | Three full traces, original provenance and H.264 display derivatives | Prior synthetic simulation work, not field data or NVIDIA output |
| Agentic Vision core `eda23d3ea646e8943287703c07a91e9a3b2909fb` | Existing perception/planner outputs through those traces | No core module imported; no new perception execution |
| Latest core inspected `5f7a821a5bebc6f1c9a70e4be9d5c4e51d947f26` | Planner and capability-specific perception trust reviewed for future extensions | Not substituted for the historical core pin or tested as part of this integration |
| Nebius repository `508238f` snapshot | Existing parser, bounded adapter and deterministic checker | Real inference reached model; successful live grounded review remains unverified |

The owner explicitly requested reuse from both owned repositories in this chat.
Their public trees do not provide a root LICENSE; public visibility alone does
not confer a redistribution license. The generated artifact folder
does not apply this repository's MIT license to the copied media/records. Before
public packaging, document the owner's chosen distribution terms and any
collaborator rights. No external core code, weights or dependencies are bundled.

AWS storage infrastructure is not copied: it adds deployment work without
solving the missing live model review. CUDA microbenchmarks cannot support a
claim that this text-review workflow is faster. The perception trust layer is
a useful next candidate for explaining revoked localization authority, but the
newest core should be pinned and evaluated separately before integration.

## Verification and remaining work

Historical baseline: 74 offline unit tests passed. Window/escaping tests added five;
local HTTP range integration adds one. Browser verification covers intrusion
37→38, GPS approval at 22, enhancement at 30 and video seeking. The generation
checks 230 per-event results against original source identities. Counts describe
engineering checks, not model accuracy or physical safety improvements.

Priority before October 30, 10:00 AM America/Los_Angeles:

1. Confirm whether the hosted service supports the requested reasoning setting.
   Attempt 004 completed one bounded live review: HTTP 200, exact model, finish
   `stop`, and matched source citation. See `verification/attempt004_public_summary.json`.
   This result does not prove hosted reasoning-disable support, model accuracy or
   physical safety. Do not relabel a deterministic fallback as model success.
2. Use separately labeled trace windows for evaluation. Include approval pending,
   action transitions, enhanced observation and nominal controls. Do not use
   this viewer's curated bookmarks as evidence of automatic model discovery.
3. Rewrite the submission around the operator's task and the demonstrated
   vision→decision→review flow. Keep compact, accurate limits and place request
   diagnostics in the technical evidence section. Explicitly identify reused
   prior work and new competition contribution.
4. Record an English demo of no more than three minutes, including at least one
   minute of modules operating for the no-hardware Physical AI submission.
   Recheck public source/demo access, license terms, final claims and submission.

Rules: https://nebiusglobalaihackathon.devpost.com/rules

PR #2 publication is complete. Attempt 004 made one paid request; no deployment,
video upload or Devpost edit was made. The OpenCV simulation, videos and traces
are disclosed prior work; this iteration adds the source-linked workbench,
bounded review windows, citation validation and Nebius review path.
