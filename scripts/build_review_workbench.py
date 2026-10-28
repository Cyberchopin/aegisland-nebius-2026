"""Build a local review workbench from existing owner-provided simulation evidence.

No core imports, inference, cloud clients, credentials or network calls.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from trace_reader import read_trace
from nebius_review import review
from model_evaluation import BaselineProvider

SOURCE_REVISION = "de93d5a25de42f00546a62c9e728ee1d8da6c5b6"
SCENARIOS = {"low_battery_intrusion": [37, 38], "gps_loss_low_light": [22, 29, 30], "nominal": [0]}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def embedded_json(value):
    # A record cannot close the inert JSON element or inject markup/script.
    return json.dumps(value, ensure_ascii=True, allow_nan=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def public_provenance(record, *, name, original_sha256, original_blob):
    """Public projection: never copy home paths, commands or environment values."""
    return {"format_version": 1, "kind": "sanitized_provenance_projection",
            "source_repository": "Cyberchopin/aegisland-opencv-2026",
            "source_revision": SOURCE_REVISION,
            "source_path": "evidence/a1/final/" + name + "/provenance.json",
            "original_sha256": original_sha256, "original_blob_sha1": original_blob,
            "core_commit": record["core_commit"], "saved_status": record["status"],
            "validation": {key: record["validation"][key] for key in
                ("trace_events", "decoded_video_frames", "all_commands_simulation_only")},
            "sha256": {"trace.jsonl": record["sha256"]["trace.jsonl"]},
            "scope": "Saved synthetic simulation; environment and filesystem metadata omitted."}


def collect(source):
    pin = json.loads((ROOT / "scripts/opencv_reuse_pin.json").read_text(encoding="utf-8"))
    if pin["revision"] != SOURCE_REVISION:
        raise ValueError("Source pin revision mismatch")
    for relative, expected in pin["blobs"].items():
        raw = (source / relative).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if blob != expected:
            raise ValueError("Source differs from pinned Git blob: " + relative)
    media = source / "submission/devpost-final-materials-20261024/media"
    media_manifest = json.loads((media / "manifest.json").read_text(encoding="utf-8"))
    scenarios, copies = [], []
    for name, bookmarks in SCENARIOS.items():
        folder = source / "evidence/a1/final" / name
        trace = folder / "trace.jsonl"
        provenance = json.loads((folder / "provenance.json").read_text(encoding="utf-8"))
        summary = read_trace(trace, include_records=True)
        if not summary["valid"] or not summary["input"]["hash_complete"]:
            raise ValueError("Invalid source trace: " + name)
        if digest(trace) != provenance["sha256"]["trace.jsonl"]:
            raise ValueError("Source trace differs from saved provenance: " + name)
        video = next(item["display_copy"] for item in media_manifest["records"] if item["scenario"] == name)
        video_path = source / video["path"]
        if digest(video_path) != video["sha256"]:
            raise ValueError("Display video hash mismatch: " + name)
        rows = []
        for entry in summary["records"]:
            line = entry["line"]
            result = review(trace, BaselineProvider(), line_window=(line, line))
            rows.append({"line": line, "record": entry["record"], "review": result})
        scenarios.append({"id": name, "bookmarks": bookmarks, "rows": rows,
                          "trace_sha256": digest(trace), "core_commit": provenance["core_commit"],
                          "video": name + "/replay.mp4", "video_sha256": video["sha256"],
                          "diagnostics": summary["diagnostics"]})
        for original, target in ((trace, "trace.jsonl"), (video_path, "replay.mp4")):
            copies.append((original, name + "/" + target, None))
        provenance_path = folder / "provenance.json"
        public_record = public_provenance(provenance, name=name,
            original_sha256=digest(provenance_path),
            original_blob=pin["blobs"][provenance_path.relative_to(source).as_posix()])
        public_bytes = (json.dumps(public_record, sort_keys=True, indent=2) + "\n").encode("utf-8")
        copies.append((provenance_path, name + "/provenance.json", public_bytes))
    return {"source_repository": "Cyberchopin/aegisland-opencv-2026", "source_revision": SOURCE_REVISION,
            "kind": "saved_synthetic_simulation_replay", "new_inference": False,
            "review_provider": "deterministic_baseline", "live_api_calls": 0,
            "scenarios": scenarios}, copies


def build(source, output):
    output = output.resolve()
    if output.exists() or output.is_relative_to(ROOT) or output.is_relative_to(source.resolve()):
        raise ValueError("Choose a fresh output folder outside both source repositories")
    data, copies = collect(source)
    template = (ROOT / "scripts/review_workbench.html").read_text(encoding="utf-8")
    template = template.replace("a.textContent='Original '+file",
        "a.textContent=file==='provenance.json'?'Public provenance summary':'Original '+file")
    output.mkdir(parents=True)
    manifest = []
    for original, target, public_bytes in copies:
        destination = output / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        if public_bytes is None:
            shutil.copyfile(original, destination)
        else:
            destination.write_bytes(public_bytes)
        if public_bytes is None and digest(original) != digest(destination):
            raise ValueError("Copy verification failed")
        item = {"source_path": original.relative_to(source).as_posix(), "output_path": target,
                "sha256": digest(destination)}
        if public_bytes is not None:
            item.update(kind="sanitized_provenance_projection", original_sha256=digest(original))
        manifest.append(item)
    (output / "reuse_manifest.json").write_text(json.dumps({
        "source_revision": SOURCE_REVISION, "files": manifest,
        "scope": "Owner-authorized reuse; prior simulation work, not new NVIDIA inference."
    }, indent=2), encoding="utf-8")
    (output / "review_data.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    (output / "index.html").write_text(template.replace("__REVIEW_DATA__", embedded_json(data)), encoding="utf-8")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Unmodified OpenCV source at the pinned revision")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = build(args.source.resolve(), args.output)
    print(json.dumps({"scenarios": len(data["scenarios"]), "validated_events": sum(
        len(s["rows"]) for s in data["scenarios"]), "live_api_calls": 0,
        "index": str((args.output / "index.html").resolve())}))


if __name__ == "__main__":
    main()
