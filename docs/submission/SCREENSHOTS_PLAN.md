# Screenshot checklist

Run the offline recording command in [DEMO_SCRIPT.md](DEMO_SCRIPT.md). Open its
fresh `demo_report.html` in a local browser; choose readable zoom and capture
actual screens. These are planned filenames, not claims that images exist.

| Capture | Frame | Required caption |
| --- | --- | --- |
| `01-trace.png` | Actual terminal `01_trace`, with hash and evidence links visible | “Synthetic trace validation and source identities.” |
| `02-baseline.png` | `02_baseline`, line 2 and approval conflict | “Deterministic no-model baseline on synthetic evidence.” |
| `03-mock.png` | `03_mock` beside `04_evaluation` | “Offline mock, not NVIDIA output; baseline 6/6 versus mock 1/6 on constructed labels.” |
| `04-live-evidence.png` | HTML saved-live section: attempts 002/003, model, HTTP 200 and both not_verified statuses | “Real Nebius-hosted NVIDIA inference succeeded; citation-grounded review did not verify.” |
| `05-reasoning-limit.png` | Attempt 003's finish length, 1,024 reasoning/completion tokens and status | “Confirmed reasoning-budget exhaustion; no successful review claimed.” |
| `06-status-cover.png` | HTML title, status banner and labeled synthetic baseline | “AegisLand — evidence review for Physical AI.” |

Keep status/limitations in the same crop as the positive claim. Do not crop away
`not_verified`, label a mock as NVIDIA output, or turn single-call latency into a
benchmark. Avoid keys, auth headers, personal tabs, billing details and shell
history. Use plain project text rather than third-party logos/music.

Save images beside the recording outputs, outside historical evidence paths.
Choose the clearest 3–5 for Devpost. Confirm their actual order and captions in
the final form; never upload a generated plan as if it were a captured screen.
