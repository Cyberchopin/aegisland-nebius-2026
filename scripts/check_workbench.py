"""Verify the shipped replay against pinned inputs and recomputed review results."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model_evaluation import BaselineProvider
from nebius_review import review
from trace_reader import read_trace


class EmbeddedData(HTMLParser):
    def __init__(self):
        super().__init__()
        self.selected = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("id") == "review-data":
            self.selected = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.selected = False

    def handle_data(self, data):
        if self.selected:
            self.parts.append(data)


def check(directory):
    directory = directory.resolve()
    pin = json.loads((ROOT / "scripts/opencv_reuse_pin.json").read_text(encoding="utf-8"))
    manifest = json.loads((directory / "reuse_manifest.json").read_text(encoding="utf-8"))
    data = json.loads((directory / "review_data.json").read_text(encoding="utf-8"))
    if data["source_revision"] != pin["revision"] or manifest["source_revision"] != pin["revision"]:
        raise ValueError("Upstream revision mismatch")
    for item in manifest["files"]:
        path = (directory / item["output_path"]).resolve()
        if not path.is_relative_to(directory):
            raise ValueError("Invalid artifact path")
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != item["sha256"]:
            raise ValueError("Artifact hash mismatch: " + item["output_path"])
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if item.get("kind") == "sanitized_provenance_projection":
            projection = json.loads(raw)
            allowed = {"format_version", "kind", "source_repository", "source_revision", "source_path",
                       "original_sha256", "original_blob_sha1", "core_commit", "saved_status",
                       "validation", "sha256", "scope"}
            if set(projection) != allowed or projection["source_path"] != item["source_path"]:
                raise ValueError("Invalid public provenance projection")
            if (projection["original_blob_sha1"] != pin["blobs"].get(item["source_path"])
                    or projection["original_sha256"] != item["original_sha256"]
                    or projection["source_revision"] != pin["revision"]):
                raise ValueError("Public provenance source identity mismatch")
        elif blob != pin["blobs"].get(item["source_path"]):
            raise ValueError("Artifact differs from pinned upstream blob")
    parser = EmbeddedData()
    parser.feed((directory / "index.html").read_text(encoding="utf-8"))
    if json.loads("".join(parser.parts)) != data:
        raise ValueError("Rendered data differs from downloadable review data")
    count = 0
    for scenario in data["scenarios"]:
        path = (directory / scenario["id"] / "trace.jsonl").resolve()
        if not path.is_relative_to(directory):
            raise ValueError("Invalid trace path")
        summary = read_trace(path, include_records=True)
        if not summary["valid"] or not summary["input"]["hash_complete"]:
            raise ValueError("Invalid trace")
        if scenario["trace_sha256"] != summary["input"]["sha256"]:
            raise ValueError("Trace identity mismatch")
        provenance = json.loads((path.parent / "provenance.json").read_text(encoding="utf-8"))
        if (provenance["sha256"]["trace.jsonl"] != summary["input"]["sha256"]
                or provenance["validation"]["trace_events"] != len(summary["records"])):
            raise ValueError("Public provenance disagrees with actual trace")
        if len(scenario["rows"]) != len(summary["records"]):
            raise ValueError("Missing or extra displayed events")
        for displayed, original in zip(scenario["rows"], summary["records"]):
            if displayed["line"] != original["line"] or displayed["record"] != original["record"]:
                raise ValueError("Displayed source record differs from original")
            line = original["line"]
            expected = review(path, BaselineProvider(), line_window=(line, line))
            if displayed["review"] != expected:
                raise ValueError("Displayed review differs from recomputed result")
            count += 1
    return {"status": "passed", "pinned_artifacts": len(manifest["files"]),
            "recomputed_event_reviews": count, "scenarios": len(data["scenarios"]),
            "live_api_calls": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(check(args.directory)))
