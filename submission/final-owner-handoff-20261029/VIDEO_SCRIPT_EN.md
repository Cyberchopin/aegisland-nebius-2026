# Video script (English) — target 2:40–2:50, hard limit under 3:00

About 360 spoken words: roughly 2:30–2:40 of speech, plus pauses for clicks. Section times are targets; the 0:35–1:45 block must be the live workbench running, uninterrupted.

---

### 0:00–0:15 · The problem
*Screen: workbench homepage.*

> A drone simulation is flying home on low battery. One frame later, it switches to an evasive hold. If you're the operator, you need to know why — and you need proof, not a guess.

### 0:15–0:35 · What AegisLand is
*Screen: hover over the three scenario cards.*

> This is AegisLand Evidence Review. It's a Physical AI review tool, not a flight controller. It takes saved simulation evidence from our OpenCV project and lets you trace every decision back to the exact record it came from. Nothing here can send a command to an aircraft.

### 0:35–1:45 · Live demo (keep the workbench on screen the whole time)
*Screen: click Low battery + intrusion → Sequence 37.*

> Here's the low-battery intrusion run. At sequence 37 the planner is returning home.

*Click Sequence 38.*

> At sequence 38, the video jumps to the exact frame, and the action changes to evade and hold. On the right is the original record: source line 39, its evidence ID, approval not required, and an execution flag that's true — in simulation. The check says it plainly: a positive flag does not prove hardware moved.

*Click "Inspect the exact source record" to expand it.*

> I can open the untouched source line and the hash of the full trace, so nothing here is a rewritten summary.

*Click "Export selected review JSON".*

> And I can export this review as JSON, with the citation attached.

*Click GPS loss + low light → Sequence 22 → Sequence 30.*

> Now GPS loss in low light. Return-to-home isn't available, so the planner asks a human for approval — and it's still pending. At sequence 30, the system takes an enhanced second look. The approval state stays visible — never mistaken for permission.

### 1:45–2:15 · Nebius Token Factory + NVIDIA Nemotron
*Screen: `verification/attempt004_public_summary.json` on GitHub.*

> Where does AI come in? We send a small, bounded window of these records to NVIDIA Nemotron on Nebius Token Factory. Nemotron has one job: pick which record to review, and which check to run. In our recorded live review, it returned HTTP 200, finished cleanly, and cited line 39 — the same moment we just looked at. Our local code verified that citation against the real file.

### 2:15–2:40 · Why it matters
*Screen: architecture diagram in the README.*

> The model points; our code checks. Malformed or uncited answers are rejected, and the model never gets a command channel. The OpenCV simulation is our earlier work; this hackathon, we built the review loop around it. For safety engineers and operators, that means fast answers they can verify.

### 2:40–2:50 · Close
*Screen: README top with the repository URL.*

> AegisLand: see why the next action changed. The code is on GitHub at Cyberchopin slash aegisland-nebius-2026. Thanks for watching.
