# Judge quickstart

**Requirements:** Python 3.11+, standard library only. No packages, no API key, no network access needed.

## Start the workbench

```sh
git clone https://github.com/Cyberchopin/aegisland-nebius-2026
cd aegisland-nebius-2026
python -B scripts/serve_review_workbench.py --directory demo --port 8090
```

On Windows you can double-click `Start_Demo.cmd` instead.

Open **http://127.0.0.1:8090/** on the same machine.

## Two things to check

1. **Low battery + intrusion** → click **Sequence 37**, then **Sequence 38**. The action changes from *return home* to *evade and hold* at **source line 39** (evidence `c71390b01d39`). The execution flag is true in simulation; hardware command sent is false.
2. **GPS loss + low light** → click **Sequence 30**. Human approval is required and still *pending*; an enhanced re-observation took place.

Expand **Inspect the exact source record** to see the original fields and full-trace SHA-256. **Export selected review JSON** downloads the review with its citation.

## Run the tests

```sh
python3 -B -m unittest discover -s tests
```

Expected: 104 tests, OK.

## The recorded live review

`verification/attempt004_public_summary.json` documents the single bounded live review: NVIDIA Nemotron 3 Super on Nebius Token Factory, HTTP 200, `finish_reason=stop`, line 39 citation validation PASS.

**You do not need to, and should not, call the live API.** The workbench and tests run fully offline. The verdicts shown in the workbench are deterministic checks, not model output.
