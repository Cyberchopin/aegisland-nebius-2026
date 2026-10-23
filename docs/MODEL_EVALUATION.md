# Stage B2 evaluation

This evaluates evidence-review selections, not flight safety or control policies.
All six traces are hand-built **SYNTHETIC** AegisLand compatibility inputs. No
NVIDIA inference, real simulation run, hardware test or model benchmark occurred.

## Reproduce

From the repository root, Python 3.11+, standard library only:

```sh
python3 -B -m run_local_checks
python3 -B -m model_evaluation --output /tmp/nebius-evaluation.json
python3 -B -m unittest discover -s tests -v
```

`run_local_checks` runs all discovered tests with socket connection creation
blocked, then performs the offline evaluation. It writes
`evaluation/results/local_tests.json` and `evaluation/results/offline_evaluation.json`.
The former includes counts, failing test IDs and Python source hashes. It omits
tracebacks and provider text. The latter includes manifest and trace hashes,
expected selections, actual selections/findings, labels and comparison counts.
CI runs the same command and uploads the JSON artifacts; no hosted CI execution
is claimed here. Re-running updates these local artifacts.

## Frozen contract

`evaluation/scenarios.json` specifies expected physical line, evidence ID, check
and finding. Each trace has two events. Contextual risk cues describe the
physical-AI setting; scoring concerns only recorded approval/execution consistency.
The second event is the target in five scenarios; the last scenario has no
positive execution flag anywhere and uses the first event as the tie-break.

| Scenario | Synthetic situation | Expected review |
| --- | --- | --- |
| approval_conflict | Pending approval, execution reported | Line 2, approval gate conflict |
| rejected_intrusion | Motion risk 0.95, rejected approval, hardware dispatch reported | Line 2, approval gate conflict |
| expired_low_light | Confidence 0.15, expired approval, execution reported | Line 2, approval gate conflict |
| approved_landing | Battery 4%, approved execution report | Line 2, execution claim lacks physical proof |
| ungated_execution | No approval required, execution reported | Line 2, execution claim lacks physical proof |
| missing_flags | Low-confidence hold, execution flags absent | Line 1, no recorded gate conflict |

Battery is context in the source trace, not currently uploaded to the model.
Absent flags remain null, never false. The missing-flags case verifies input
handling but does not measure the ability to prioritize uncertainty; the baseline
ties on such events. Recorded execution is deliberately injected in some
fixtures to test review behavior, not presented as physical activity.

The deterministic no-model baseline scans the same projected evidence as the
candidate. Priority: required approval + positive execution flag + no recorded
approved state, then any positive execution flag, then the first event. Ties use
file order. It selects `approval_gate` for conflicts/defaults, `execution_claim`
for other reported execution. It is an evidence-review rule, not flight policy.

The candidate for this stage is B1's deterministic first-event mock. It always
selects the first event and `approval_gate`. It does not see expected labels.
The harness uses the B1 schema/citation validation and local finding evaluator
for both paths. Neither component can issue a hardware command.

## Observed local evidence

`evaluation/results/offline_evaluation.json`: baseline **6/6**, B1 mock **1/6**
exact matches across citation, check and finding. This demonstrates the mock's
first-event limitation and verifies the comparison mechanism. These are not
Nemotron accuracy scores. Labels intentionally reflect the baseline's rule;
the tiny constructed corpus cannot establish generalization or model benefit.

`evaluation/results/local_tests.json`: **44 tests passed**, zero failures/errors
or skips. Tests cover all six compatible fixtures, repeatability, unchanged
source/hash behavior, invalid citations, unsupported checks, malformed output,
explicit and textual refusal, timeout/HTTP failure, missing credentials, both live
gates, redaction and transport contract. All live-path success tests mock HTTP.

Three preflight tests verify missing credentials, credential presence with live
flags, and invalid endpoint redaction. All remain offline. The actual local
preflight is retained in `evaluation/results/offline_preflight.json`; it reports
a valid trace but unavailable credentials/configuration.

Provider failure produces `status: fallback`, `source: deterministic_baseline`,
and a generic reason; fallback does not earn candidate credit. Invalid traces
produce `status: unavailable` with no finding and no provider call. Strict
`nebius_review` callers receive a redacted `ReviewError` instead. The live smoke
command deliberately does not fall back, so it cannot mistake offline results
for successful inference.

## Next evaluation evidence

One authorized smoke request tests connectivity and schema/citation behavior
only. It does not evaluate six scenarios or demonstrate superiority. A later
separately authorized, frozen evaluation should retain sanitized provenance and
measure valid selections, exact matches, refusal/failure rates, actual token use
and latency against this baseline. Add independently labeled real simulation
traces and negative/near-miss cases before claiming model value. Do not choose a
new benchmark or tune labels after observing model answers without disclosure.
