# Video shot list — target 2:50, under 3:00

Continuous running-module footage: **0:35–1:45 (70 s)**, workbench only, no cuts to slides.

| Time | Screen | Mouse action | Narration | Evidence that must appear | Risk |
| --- | --- | --- | --- | --- | --- |
| 0:00–0:15 | Workbench homepage | None | 1 · The problem | Title "See why the next action changed." | Close other tabs; no bookmarks bar |
| 0:15–0:35 | Scenario cards, stats 3 / 230 / 0 | Hover over the three cards | 2 · What AegisLand is | "OFFLINE REPLAY" badge | Say "not a flight controller" |
| 0:35–0:50 | Low battery + intrusion | Click scenario → **Sequence 37** | 3a | Action: return home | Wait for video to seek before speaking |
| 0:50–1:10 | Same, sequence 38 | Click **Sequence 38**; point at facts | 3b | evade and hold · source line 39 · `c71390b01d39` · Execution flag true · Hardware command sent false | Do not call the verdict "model output" |
| 1:10–1:18 | Source record card | Scroll a little; expand **Inspect the exact source record** | 3c | Original fields + full-trace SHA-256 | **Stop scrolling here** — the Integration status panel below has outdated text |
| 1:18–1:25 | Evidence panel | Click **Export selected review JSON ↓** | 3d | Download of review JSON | Download bar must not show private folder paths |
| 1:25–1:45 | GPS loss + low light | Click scenario → **Sequence 22** → **Sequence 30** | 3e | request human approval · approval pending · active re-observation true | Keep the workbench on screen |
| 1:45–2:15 | GitHub: `verification/attempt004_public_summary.json` | Point at `http_status`, `model`, `finish_reason`, `"line": 39`, `citation_validation` | 4 · Nebius + Nemotron | HTTP 200 · nvidia/nemotron-3-super-120b-a12b · stop · PASS · 388/40 | Never show receipts, request IDs, keys or the Nebius console |
| 2:15–2:40 | GitHub README Architecture diagram | Scroll to the diagram | 5 · Why it matters | "Never allowed: flight commands" box | Merge the README PR first, or the old README shows |
| 2:40–2:50 | README top | Scroll to top | 6 · Close | Repository URL | Stop recording before 3:00 |
