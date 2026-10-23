# Record the demonstration — 2 minutes 45 seconds

Use the existing results. No API key or live request is needed. Run from the
repository root in WSL; choose an output directory that does not already exist:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/demo_runbook.py --output-dir /tmp/aegisland-recording-01 --interactive
```

The executable runbook blocks networking/live provider calls, pauses before each
module, and writes JSON plus `demo_report.html` outside the repository. It checks
all historical evidence hashes before/after operation. It refuses a reused output
directory. Do not redirect over historical evidence or rerun a consumed smoke test.

Before recording: close unrelated windows, hide shell history and turn off desktop
notifications. No terminal, browser tab or recording may show a key or card data.
Use an ordinary screen recorder on Windows or WSL. Include narration/captions in
English. Do not record a billing dashboard. Start the recorder before the first
module and pause at the runbook prompts to explain the output.

| Time | Show and operate | Say |
| --- | --- | --- |
| 0:00–0:20 | README title/current status | “AegisLand helps simulation operators inspect recorded evidence. NVIDIA inference runs on Nebius. The live evidence review still has not verified.” |
| 0:20–0:45 | Open the fixed `evaluation/traces/approval_conflict.jsonl`; show source lines 1 and 2 | “This input is synthetic. Event 2 reports execution while approval is pending. These are recorded flags, not evidence of physical flight.” |
| 0:45–1:05 | Press Enter for `01_trace`; point to evidence links and SHA-256 | “The reader validates the trace and preserves physical source lines and evidence identities.” |
| 1:05–1:25 | Press Enter for `02_baseline`; show line 2 and the conflict finding | “The deterministic baseline finds the recorded approval conflict without a model.” |
| 1:25–1:40 | Show `03_mock` then `04_evaluation` | “This is an offline mock, not NVIDIA output. It selects the first event. Across six synthetic cases the baseline matches six labels; this mock matches one.” |
| 1:40–2:10 | Show `05_saved_live_evidence`; highlight attempts 002 and 003 together | “The retained real requests reached Nemotron 3 Super with HTTP 200. The review did not verify. Attempt 003 used all 1,024 output tokens for reasoning and stopped at the limit.” |
| 2:10–2:30 | Show `06_preservation` and B4 test evidence | “We preserved every result and consumed guard. Offline tests cover parser, citation and failure handling. A non-thinking configuration is blocked until Nebius confirms support.” |
| 2:30–2:45 | Show the generated HTML status banner | “Real model integration is demonstrated. Live citation grounding remains unverified. Model recommendations cannot issue flight commands.” |

The 0:20–1:40 segment is 80 seconds of key modules/input inspection in operation.
Keep actual module interaction visible; do not replace it with a slide montage.
For screenshots after recording, open the generated HTML locally. In WSL,
`wslpath -w /tmp/aegisland-recording-01/demo_report.html` gives its Windows path;
copy that ordinary file path into your browser. No server or deployment is needed.

Review the video frame by frame for secrets, visible labels, legibility and sound.
Upload the actual finished video publicly to YouTube, then paste its URL into
the Devpost draft. The runbook generates neither a video nor screenshots; those
must be recorded/captured by the owner. Read the [submission checklist](SUBMISSION_CHECKLIST.md).
