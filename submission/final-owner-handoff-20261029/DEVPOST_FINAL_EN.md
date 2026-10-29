# Devpost final copy (English)

Copy each section into the matching Devpost field. See `DEVPOST_FIELD_MAP_ZH.md` for the field-by-field guide.

---

## Project name

AegisLand — Evidence Review for Physical AI

## One-line tagline

See why a simulated drone changed its next action, and prove it from the source line.

## Short description

AegisLand turns saved Physical AI simulation evidence into a source-linked review workflow. NVIDIA Nemotron on Nebius Token Factory picks one evidence record and one allowed check; local code validates the citation and judges the recorded fact, without ever issuing a flight command.

---

## Inspiration

A drone simulation is returning home on low battery. One frame later, it switches to an evasive hold. The operator's first question is simple: **why?** Which observation changed? Did the action need human approval? Does "executed" mean the simulation acted, or that hardware actually moved?

Logs answer those questions only if someone can find the right line. We wanted a review tool where every claim points back to the exact record it came from, and where an AI model helps an operator look in the right place without ever being trusted to act.

## What it does

AegisLand is an evidence workbench for Physical AI. An operator picks a saved scenario (nominal mission, low battery with an intrusion, or GPS loss in low light), jumps to a key moment, and the replay video seeks to that frame. Next to it, the workbench shows the original trace line behind the decision: the recorded action and reason, evidence ID, approval state, execution flag, motion risk and whether an enhanced re-observation happened. A deterministic check states what the recorded fact does and does not establish, for example that an execution flag in simulation does not prove a motor turned. Every review can be exported as JSON with its line number, evidence ID and the SHA-256 of the full source trace.

On top of that, a bounded review path lets NVIDIA Nemotron, served through Nebius Token Factory, choose which record to look at and which check to run. The model only points; local code verifies the pointer and evaluates the fact.

## How we built it

Everything runs on Python's standard library, so judges can start the workbench with no installs and no API key. The trace reader validates each JSONL simulation trace and hashes it. A bounded projection keeps a small window of original source lines (at most 32 records and 32 KiB) with their real line numbers. HTML and JavaScript provide scenario selection, a clickable event timeline, frame-accurate video seeking and JSON export. A pinned importer verifies upstream Git blob identities and video hashes before building the workbench, so the bundled evidence is byte-for-byte the original.

## How Nebius Token Factory is used

Nebius Token Factory serves the model through its OpenAI-compatible chat completions endpoint. Our adapter sends one bounded evidence window and a strict instruction: return JSON naming exactly one cited event and one allowed check. Token Factory's response metadata (returned model, token usage and finish reason) is recorded with every attempt; that metadata is what let us diagnose earlier failures and confirm the successful run.

## How NVIDIA Nemotron is used

`nvidia/nemotron-3-super-120b-a12b` acts as an evidence selector. Given a window of simulation records, it chooses which single record deserves review and whether to run `approval_gate` or `execution_claim`. In our recorded live review (Attempt 004), Nemotron returned HTTP 200 with `finish_reason=stop`, cited source line 39 (evidence `c71390b01d39`) and selected `execution_claim`. Local validation confirmed the citation matched a real record, using 388 input and 40 output tokens.

## How OpenCV evidence is used

The scenarios come from the existing AegisLand OpenCV 5 simulation: edge structure, texture risk, optical flow and CLAHE re-observation produced 3 replays and 230 trace events. AegisLand Evidence Review treats those saved outputs as evidence to be inspected, not re-run. The videos are display derivatives of the saved simulation, and every event links back to its original line.

## Challenges we ran into

Reaching a model turned out to be very different from getting a usable review. Our first live attempt failed authentication. The next two reached Nemotron and returned HTTP 200, but neither produced a valid citation; in the third, all 1,024 output tokens were spent on reasoning and the response ended with `finish_reason=length`. We kept all three failures on record, analysed them, tightened the request, and made exactly one more attempt, which succeeded.

The other challenge was keeping citations trustworthy on long traces. We validate the full source file first, then project a small window without renumbering, so a citation to line 39 always means line 39 of the original file.

## Accomplishments that we're proud of

- A working offline workbench that connects 230 recorded events to video frames, source lines and exportable reviews.
- A model integration where the model has no command channel: malformed or uncited output is rejected, and nothing it returns can trigger an action.
- One bounded live Nemotron review that passed citation validation, with every earlier failure preserved instead of overwritten.
- 104 offline tests passing, all 230 workbench reviews recomputed from original lines, and 29 historical evaluation files unchanged.

## What we learned

A successful API call is not a successful review. Finish reasons, token usage and citation checks matter more than a 200 status. We also learned that the most useful thing a model can do in a safety-relevant review is narrow the operator's attention, while deterministic code does the judging.

## What's next

Evaluate Nemotron's selections against independently labeled simulation windows and compare them with the no-model baseline. Confirm a hosted configuration for non-thinking structured output. Extend the workbench to more scenarios and to traces from the upcoming GPS-denied navigation work.

## Existing work and significant updates during the hackathon

**Existing work (disclosed):** the AegisLand OpenCV perception stack, deterministic planner and the three recorded simulation runs with 230 trace events come from earlier AegisLand projects (`aegisland-agentic-vision`, core pinned at `eda23d3`, and `aegisland-opencv-2026`). They are synthetic simulation, not new flight footage.

**New during this hackathon:**
- Nebius Token Factory + NVIDIA Nemotron review path.
- Strict JSON parsing and citation validation.
- Bounded evidence windows that preserve original line numbers and full-trace hashes.
- The interactive source-linked review workbench.
- Approval and execution consistency checks.
- Public-safe provenance summaries.
- A deterministic fallback, with every failed live attempt retained.

## Built With

Python (standard library), HTML, JavaScript, JSONL, SHA-256, unittest, GitHub Actions, Nebius Token Factory, NVIDIA Nemotron 3 Super. OpenCV 5 simulation is disclosed reused work.

## Testing instructions

1. Clone https://github.com/Cyberchopin/aegisland-nebius-2026 (Python 3.11+, no packages, no API key).
2. From the repository root run `python -B scripts/serve_review_workbench.py --directory demo --port 8090`, or double-click `Start_Demo.cmd` on Windows.
3. Open http://127.0.0.1:8090/ in a browser on the same machine.
4. Choose **Low battery + intrusion**, click **Sequence 37**, then **Sequence 38**. The decision changes from return home to evade and hold at source line 39.
5. Choose **GPS loss + low light**, click **Sequence 30** to see a pending approval with active re-observation.
6. Run the tests with `python3 -B -m unittest discover -s tests`.
7. The recorded live review is in `verification/attempt004_public_summary.json`. Judges do not need to, and should not, call the live API.

## Repository URL

https://github.com/Cyberchopin/aegisland-nebius-2026

## Suggested track

Physical AI

## Nebius / NVIDIA feedback

- **What worked well:** Token Factory's OpenAI-compatible endpoint made the adapter small. Returned model identity, token usage and `finish_reason` were exactly what we needed to diagnose a truncated review.
- **What tripped us up:** with Nemotron 3 Super, one attempt spent its entire 1,024-token budget on reasoning and returned no usable answer. NVIDIA documents non-thinking controls, but we could not confirm from the hosted docs whether Token Factory honors them for this model.
- **Suggestions:** a model-specific example for short structured-JSON tasks with reasoning disabled, a documented way to confirm which reasoning mode was applied, and clearer guidance on authentication errors would save teams real time.

## Honest limitations

- All scenarios are synthetic simulation; no real drone hardware was operated.
- Attempt 004 is one bounded live review. It does not measure model accuracy or establish flight certification, production safety or a long-running service.
- The verdicts shown in the workbench are deterministic checks, not model output.
- There is no always-on public API endpoint; the API key has been deleted.
- Hosted support for the requested reasoning setting remains unconfirmed.
