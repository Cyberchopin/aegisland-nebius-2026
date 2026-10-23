# Owner actions to record and submit

The local package is prepared. No push, deployment, upload or Devpost submission
has been performed. Live model integration succeeded; live citation review remains
`not_verified`. Keep that statement in every submitted version.

## Record

1. Review the README, evidence table and MIT license. Confirm ownership of the
   contributions and permission for any media you plan to use.
2. Open a clean local terminal in this repository. No API key is needed. Start
   your screen recorder, then follow [DEMO_SCRIPT.md](DEMO_SCRIPT.md), running:

   ```sh
   python3 -B scripts/demo_runbook.py --output-dir /tmp/aegisland-recording-01 --interactive
   ```

   Use a fresh output path if it exists. Keep at least 80 seconds of actual module
   interaction from the script; narrate the saved live evidence honestly.
3. Capture the [screenshots](SCREENSHOTS_PLAN.md), review redaction/audio/labels,
   export the actual video and upload it publicly to YouTube. Copy its final URL.

## Publish only after your review

4. Review all pending files and changes in `codex-b/stage-b1-nebius`. The new work
   is local and largely uncommitted. Authorize a reviewed commit/push/merge
   explicitly, or publish it yourself. Confirm the public submission URL contains
   the final code, MIT license, synthetic fixtures and all historical evidence.
   Verify GitHub detects MIT. Do not upload .env files, caches or credentials.
5. Test the public source's offline commands from a clean checkout. Judges must
   receive the complete working test build and instructions. Do not include an
   API key in the repository or submission; arrange any live judging access
   separately without granting another inference in this task.

## Enter Devpost

6. Join/sign into the event, confirm eligibility and team representation, then
   select the proposed Physical AI track after checking its fit. Fill personal
   names, team members, any city-event details and the two actual URLs in
   [DEVPOST_DRAFT.md](DEVPOST_DRAFT.md). Confirm significant-update dates and rights.
7. Paste the prepared sections, add the video URL and selected screenshots, and
   complete the current form's required fields. Preview it as a judge. Ensure
   the unverified review and synthetic mock labels remain visible.
8. Submit before **October 30, 2026, 10:00 AM PDT / 17:00 UTC**, preferably a day
   early. Confirm Devpost shows a submitted entry rather than a draft and retain
   its confirmation URL. Keep the project accessible for judging.

## Official requirements checked

The [official rules](https://nebiusglobalaihackathon.devpost.com/rules) require
Nebius runtime use plus an NVIDIA open-source model; a public, licensed source
repository with setup instructions; track selection, tool feedback, and disclosure
of significant updates to an existing project. Video should be under three
minutes, public on YouTube, with at least one minute showing hardware or, for a
no-hardware Physical AI project, key modules operating. English materials or
translations are required. Physical AI has a demo-URL exception, but judging
access still applies. Judging ends December 15, 2026, at noon Pacific. Owner
eligibility, conflicts, rights and form completeness require personal confirmation.
These checks do not guarantee organizer acceptance of this prototype's track fit
or incomplete live-review functionality.
