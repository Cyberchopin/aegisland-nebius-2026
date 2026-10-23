#!/usr/bin/env python3
"""Offline-only recording runbook. Writes fresh demo artifacts outside the repository."""
import argparse
import hashlib
import html
import json
import math
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model_evaluation import BaselineProvider, evaluate
from nebius_review import MODEL, MockProvider, review
from trace_reader import read_trace


def hashes():
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (ROOT / "evaluation").rglob("*") if p.is_file()}


def sanitized_live(path):
    record = json.loads(path.read_text())
    result = {"source": "saved_owner_run_live_evidence", "file": path.name,
              "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    for key, allowed in {
        "status": ("verified", "not_verified"), "response_model": (MODEL,),
        "finish_reason": ("stop", "length", "content_filter", "unrecognized"),
        "failure_code": ("response_truncated", "invalid_selection_json", "citation_mismatch"),
    }.items():
        result[key] = record.get(key) if record.get(key) in allowed else None
    for key in ("http_status", "elapsed_latency_ms", "estimated_cost_usd"):
        value = record.get(key)
        result[key] = value if type(value) in (int, float) and math.isfinite(value) and value >= 0 else None
    result["usage"] = {key: value for key, value in (record.get("usage") or {}).items()
                       if key in ("prompt_tokens", "completion_tokens", "total_tokens")
                       and type(value) is int and 0 <= value <= 10000000}
    details = record.get("token_details", {}).get("completion_tokens_details", {})
    value = details.get("reasoning_tokens")
    result["reasoning_tokens"] = value if type(value) is int and 0 <= value <= 10000000 else None
    result["citation_valid_recorded"] = record.get("citation_valid") is True
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True, help="A NEW directory outside this repo")
    parser.add_argument("--interactive", action="store_true", help="Pause between modules for recording")
    args = parser.parse_args(argv)
    output = args.output_dir.resolve()
    if output.is_relative_to(ROOT):
        parser.error("Output directory must be outside the repository to preserve evidence")
    if output.exists():
        parser.error("Output directory must not already exist; choose a fresh path")
    output.mkdir(parents=True)
    before = hashes()

    def show(name, value):
        if args.interactive:
            input("Press Enter to show " + name + " (offline). ")
        print("\n" + name)
        print(json.dumps(value, sort_keys=True, indent=2, allow_nan=False))
        (output / (name + ".json")).write_text(json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n")

    with patch("socket.create_connection", side_effect=RuntimeError("Demo networking disabled")), patch(
            "nebius_review.NebiusProvider.complete", side_effect=RuntimeError("Live inference disabled in demo")):
        trace = ROOT / "evaluation/traces/approval_conflict.jsonl"
        summary = read_trace(trace)
        show("01_trace", {"label": "SYNTHETIC TRACE VALIDATION", "valid": summary["valid"],
                          "input_sha256": summary["input"]["sha256"], "evidence_links": summary["evidence_links"]})
        baseline = review(trace, BaselineProvider())
        show("02_baseline", {"label": "SYNTHETIC / NO MODEL", "selection": baseline["selection"],
                              "finding": baseline["finding"]})
        mock = review(trace, MockProvider())
        show("03_mock", {"label": "SYNTHETIC / OFFLINE MOCK — NOT NVIDIA OUTPUT",
                          "selection": mock["selection"], "finding": mock["finding"]})
        evaluation = evaluate()
        show("04_evaluation", {key: evaluation[key] for key in (
            "synthetic", "candidate_provider", "actual_nvidia_inference", "live_api_calls",
            "scenario_count", "baseline_matches", "candidate_matches")})
        live = [sanitized_live(ROOT / "evaluation/results" / name) for name in
                ("live_smoke.json", "live_smoke_002.json", "live_smoke_003.json")]
        show("05_saved_live_evidence", live)
    unchanged = before == hashes()
    show("06_preservation", {"all_historical_evidence_unchanged": unchanged,
                              "protected_files": len(before), "new_api_calls": 0})
    cards = [("Synthetic baseline", baseline["selection"], baseline["finding"]),
             ("Offline mock — not NVIDIA output", mock["selection"], mock["finding"])]
    content = "".join("<section><h2>" + html.escape(title) + "</h2><pre>" +
                      html.escape(json.dumps(selection, indent=2)) + "</pre><p>" + html.escape(finding) +
                      "</p></section>" for title, selection, finding in cards)
    content += "<section><h2>Saved real inference evidence</h2><pre>" + html.escape(json.dumps(live, indent=2)) + "</pre></section>"
    page = """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>AegisLand submission demo</title><style>body{font:18px system-ui;margin:40px auto;max-width:1000px;padding:0 24px;background:#101827;color:#e5edf7}h1{font-size:36px}section{background:#1b2940;padding:20px;margin:22px 0;border-radius:10px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:15px}.status{border-left:5px solid #f5ba55;padding:15px;background:#263148}</style>
<h1>AegisLand — evidence review for Physical AI</h1><p class="status">Real Nebius-hosted NVIDIA inference succeeded. Live citation-grounded review remains not_verified.</p>
<p>Offline recording artifact. No new API call, no hardware command. Synthetic baseline/mock results are labeled below.</p>""" + content + "</html>"
    (output / "demo_report.html").write_text(page)
    print("\nOpen locally for screenshots: " + str(output / "demo_report.html"))
    return 0 if unchanged else 1


if __name__ == "__main__":
    raise SystemExit(main())
