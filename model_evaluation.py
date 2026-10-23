"""Offline synthetic evaluation. No network-capable provider is constructed here."""
import argparse
import hashlib
import json
from pathlib import Path

from nebius_review import MockProvider, ReviewError, review

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "evaluation/scenarios.json"


class BaselineProvider:
    """No-model review priority: approval conflict, execution report, first event."""
    def complete(self, messages):
        events = json.loads(messages[1]["content"])
        def priority(event):
            reported = event["command_executed"] is True or event["hardware_command_sent"] is True
            conflict = reported and event["requires_human_approval"] and event["approval_status"] != "approved"
            return 2 if conflict else 1 if reported else 0
        event = max(events, key=priority)  # Stable file-order tie break.
        check = "approval_gate" if priority(event) != 1 else "execution_claim"
        return json.dumps({"line": event["line"], "evidence_id": event["evidence_id"], "check": check})


def safe_review(path, provider):
    """A provider failure never becomes a clean model result or a flight command."""
    try:
        return {"status": "reviewed", "source": "candidate", "result": review(path, provider)}
    except ReviewError:
        try:
            return {"status": "fallback", "source": "deterministic_baseline",
                    "reason": "candidate_unavailable_or_invalid",
                    "result": review(path, BaselineProvider())}
        except ReviewError:
            return {"status": "unavailable", "source": None, "result": None,
                    "reason": "trace_not_reviewable", "hardware_action": False}


def evaluate():
    manifest_bytes = MANIFEST.read_bytes()
    manifest = json.loads(manifest_bytes)
    rows = []
    for scenario in manifest["scenarios"]:
        path = MANIFEST.parent / scenario["trace"]
        expected = scenario["expected"]
        baseline = review(path, BaselineProvider())
        candidate = safe_review(path, MockProvider())
        result = candidate["result"]
        def matches(value):
            return value is not None and all(
                (value["finding"] if key == "finding" else value["selection"][key]) == item
                for key, item in expected.items())
        rows.append({"scenario": scenario["id"], "trace_sha256": baseline["input_sha256"],
                     "expected": expected,
                     "baseline": {"selection": baseline["selection"], "finding": baseline["finding"],
                                  "matches_expected": matches(baseline)},
                     "candidate": {"status": candidate["status"], "source": candidate["source"],
                                   "selection": result["selection"] if result else None,
                                   "finding": result["finding"] if result else None,
                                   "matches_expected": candidate["status"] == "reviewed" and matches(result)}})
    return {"format_version": 1, "synthetic": True, "candidate_provider": "B1_first_event_mock",
            "actual_nvidia_inference": False, "live_api_calls": 0,
            "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            "scenario_count": len(rows),
            "baseline_matches": sum(row["baseline"]["matches_expected"] for row in rows),
            "candidate_matches": sum(row["candidate"]["matches_expected"] for row in rows),
            "rows": rows}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = evaluate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
