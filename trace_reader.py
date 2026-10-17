"""Standard-library compatibility reader for unversioned AegisLand JSONL traces."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import sys

ACTIONS = frozenset({"continue_mission", "return_home", "hold_and_scan", "evade_and_hold",
                     "request_human_approval", "land", "emergency_land", "emergency_recovery"})
SAFETY_LEVELS = frozenset({"nominal", "caution", "high", "critical"})
COMMAND_STATUSES = frozenset({"simulated", "awaiting_human_approval", "approval_rejected",
                             "approval_expired", "timeout", "failed"})
LIFECYCLE_STATUSES = frozenset({"planned", "dispatched", "acknowledged", "completed", "timeout", "failed"})
APPROVAL_STATUSES = frozenset({"requested", "pending", "approved", "rejected", "expired"})


def _number(value):
    try:
        return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)
    except OverflowError:
        return False


def _integer(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def _float(text):
    value = float(text)
    if not math.isfinite(value):
        raise ValueError("non-finite JSON number")
    return value


def _constant(_):
    raise ValueError("non-finite JSON constant")


def _validate(record, emit):
    """Validate the required compatibility subset without changing the original dict."""
    def require(value, predicate, field):
        if not predicate(value):
            emit("error", "invalid_field", field, "Missing or invalid required field.")

    def known(value, allowed, field):
        if _text(value) and value not in allowed:
            emit("warning", "unknown_value", field, "Unrecognized value retained; no success inferred.")

    require(record.get("trace_id"), _text, "trace_id")
    require(record.get("sequence"), _integer, "sequence")
    for field in ("telemetry", "evidence", "decision", "command"):
        require(record.get(field), lambda x: isinstance(x, dict), field)
    telemetry = record.get("telemetry")
    if isinstance(telemetry, dict):
        require(telemetry.get("battery_percent"), lambda x: _number(x) and 0 <= x <= 100,
                "telemetry.battery_percent")
        require(telemetry.get("altitude_m"), lambda x: _number(x) and x >= 0, "telemetry.altitude_m")
        for field in ("timestamp_s", "horizontal_speed_mps"):
            if field in telemetry:
                require(telemetry[field], lambda x: _number(x) and x >= 0, "telemetry." + field)
        for field in ("gps_available", "home_link_available"):
            if field in telemetry:
                require(telemetry[field], lambda x: isinstance(x, bool), "telemetry." + field)
    evidence = record.get("evidence")
    if isinstance(evidence, dict):
        require(evidence.get("evidence_id"), _text, "evidence.evidence_id")
        require(evidence.get("frame_index"), _integer, "evidence.frame_index")
        for field in ("confidence", "obstacle_risk", "motion_risk"):
            require(evidence.get(field), lambda x: _number(x) and 0 <= x <= 1, "evidence." + field)
    for name in ("decision", "raw_decision"):
        decision = record.get(name)
        if name == "raw_decision" and decision is None:
            continue
        if not isinstance(decision, dict):
            if name == "raw_decision":
                emit("error", "invalid_field", name, "Expected an object or null.")
            continue
        for field in ("action", "safety_level", "evidence_id"):
            require(decision.get(field), _text, name + "." + field)
        require(decision.get("risk_score"), lambda x: _number(x) and 0 <= x <= 1, name + ".risk_score")
        require(decision.get("requires_human_approval"), lambda x: isinstance(x, bool), name + ".requires_human_approval")
        require(decision.get("reasons"), lambda x: isinstance(x, list) and all(isinstance(v, str) for v in x), name + ".reasons")
        if "command_executed" in decision:
            require(decision["command_executed"], lambda x: isinstance(x, bool), name + ".command_executed")
        known(decision.get("action"), ACTIONS, name + ".action")
        known(decision.get("safety_level"), SAFETY_LEVELS, name + ".safety_level")
        if isinstance(evidence, dict) and _text(decision.get("evidence_id")) and _text(evidence.get("evidence_id")):
            if decision["evidence_id"] != evidence["evidence_id"]:
                emit("error", "evidence_mismatch", name + ".evidence_id", "Decision does not reference this event's evidence.")
    command = record.get("command")
    if isinstance(command, dict):
        require(command.get("status"), _text, "command.status")
        known(command.get("status"), COMMAND_STATUSES, "command.status")
        if "command_status" in command:
            require(command["command_status"], _text, "command.command_status")
            known(command["command_status"], LIFECYCLE_STATUSES, "command.command_status")
        if "hardware_command_sent" in command:
            require(command["hardware_command_sent"], lambda x: isinstance(x, bool), "command.hardware_command_sent")
        if "approval_id" in command or "approval_status" in command:
            require(command.get("approval_id"), _text, "command.approval_id")
            require(command.get("approval_status"), _text, "command.approval_status")
            known(command.get("approval_status"), APPROVAL_STATUSES, "command.approval_status")
        elif isinstance(record.get("decision"), dict) and record["decision"].get("requires_human_approval") is True:
            emit("warning", "approval_metadata_missing", "command", "Approval required, but no recorded approval ID/status is available.")
    if "schema_version" in record:
        emit("warning", "unversioned_compatibility", "schema_version", "Input declares a version; this reader only validates its documented compatibility subset.")


def _lines(stream, digest, limit):
    """Hash every byte, consuming oversized lines in bounded chunks rather than truncating the hash."""
    while True:
        raw = stream.readline(limit + 1)
        if not raw:
            return
        digest.update(raw)
        size = len(raw)
        oversized = size > limit
        while not raw.endswith(b"\n") and len(raw) == limit + 1:
            raw = stream.readline(limit + 1)
            if not raw:
                break
            digest.update(raw)
            size += len(raw)
            oversized = True
        yield None if oversized else raw


def read_trace(path, *, include_records=False, max_line_bytes=1024 * 1024):
    """Read exactly the supplied file; return JSON-safe summary and line-numbered diagnostics.

    No input is rewritten. Unknown fields survive in optional included records.
    Exact duplicate event IDs are excluded from aggregates; conflicting duplicates
    are errors and excluded after the first record. State changes follow file order.
    """
    if isinstance(max_line_bytes, bool) or not isinstance(max_line_bytes, int) or max_line_bytes < 1:
        raise ValueError("max_line_bytes must be a positive integer")
    result = {
        "reader_format_version": 1, "input": {"path": str(Path(path).resolve()), "sha256": None, "hash_complete": False},
        "valid": True, "diagnostics": [], "diagnostic_counts": {"error": 0, "warning": 0},
        "counts": {"lines": 0, "blank_lines": 0, "parse_errors": 0, "invalid_records": 0,
                   "included_records": 0, "duplicate_event_records": 0, "conflicting_event_records": 0},
        "final_decisions": Counter(), "raw_decisions": Counter(), "raw_decision_missing_or_null": 0,
        "command_statuses": Counter(), "command_lifecycle_statuses": Counter(),
        "reported_execution_flags": {"decision_command_executed": Counter(), "hardware_command_sent": Counter()},
        "decision_reasons": Counter(), "raw_decision_reasons": Counter(), "safety_levels": Counter(),
        "maximum_recorded_risk_score": None, "required_approval_decision_records": 0,
        "approvals": {"unique_count": 0, "observations": 0, "state_change_count": 0,
                      "repeated_state_records": 0, "duplicate_event_records": 0, "items": []},
        "evidence_links": [], "traces": [],
    }
    if include_records:
        result["records"] = []
    def diagnostic(line, severity, code, field, message):
        result["diagnostics"].append({"line": line, "severity": severity, "code": code, "field": field, "message": message})
        result["diagnostic_counts"][severity] += 1
        if severity == "error":
            result["valid"] = False

    seen, highwater, trace_counts, approvals = {}, {}, Counter(), {}
    digest = hashlib.sha256()
    try:
        with Path(path).open("rb") as stream:
            before = os.fstat(stream.fileno())
            if not stat.S_ISREG(before.st_mode):
                raise OSError("Input must be a regular file")
            for line, raw in enumerate(_lines(stream, digest, max_line_bytes), 1):
                result["counts"]["lines"] += 1
                if raw is None:
                    result["counts"]["parse_errors"] += 1
                    diagnostic(line, "error", "line_too_long", "", "Line exceeds max_line_bytes; all bytes still contribute to SHA-256.")
                    continue
                if not raw.strip():
                    result["counts"]["blank_lines"] += 1
                    diagnostic(line, "warning", "blank_line", "", "Blank line ignored.")
                    continue
                try:
                    record = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                                        parse_float=_float, parse_constant=_constant)
                except (UnicodeDecodeError, ValueError, RecursionError) as error:
                    result["counts"]["parse_errors"] += 1
                    diagnostic(line, "error", "invalid_json", "", type(error).__name__ + ": invalid UTF-8/JSON, ambiguous keys or non-finite numbers.")
                    continue
                if not isinstance(record, dict):
                    result["counts"]["invalid_records"] += 1
                    diagnostic(line, "error", "invalid_record", "", "Expected a JSON object.")
                    continue
                previous_errors = result["diagnostic_counts"]["error"]
                _validate(record, lambda severity, code, field, message: diagnostic(line, severity, code, field, message))
                if result["diagnostic_counts"]["error"] != previous_errors:
                    result["counts"]["invalid_records"] += 1
                    continue
                trace, sequence = record["trace_id"], record["sequence"]
                event_key = trace, sequence
                fingerprint = hashlib.sha256(json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode()).hexdigest()
                command = record["command"]
                approval_key = (trace, command["approval_id"]) if "approval_id" in command else None
                if event_key in seen:
                    if fingerprint == seen[event_key]:
                        result["counts"]["duplicate_event_records"] += 1
                        diagnostic(line, "warning", "duplicate_event", "sequence", "Identical event already observed; excluded from aggregates.")
                        if approval_key is not None:
                            result["approvals"]["duplicate_event_records"] += 1
                            approvals[approval_key]["duplicate_event_records"] += 1
                    else:
                        result["counts"]["conflicting_event_records"] += 1
                        diagnostic(line, "error", "conflicting_event", "sequence", "Same trace_id/sequence has different content; later record excluded.")
                    continue
                seen[event_key] = fingerprint
                if trace not in highwater:
                    if sequence != 0:
                        diagnostic(line, "warning", "sequence_nonzero_start", "sequence", "Trace begins at a nonzero sequence; earlier events may be absent.")
                elif sequence < highwater[trace]:
                    diagnostic(line, "warning", "sequence_out_of_order", "sequence", "Unique event is behind the previously observed high-water sequence.")
                elif sequence > highwater[trace] + 1:
                    diagnostic(line, "warning", "sequence_gap", "sequence", "Sequence gap after " + str(highwater[trace]) + ".")
                highwater[trace] = max(sequence, highwater.get(trace, sequence))
                trace_counts[trace] += 1
                result["counts"]["included_records"] += 1
                decision, evidence = record["decision"], record["evidence"]
                result["final_decisions"][decision["action"]] += 1
                result["decision_reasons"].update(set(decision["reasons"]))
                result["safety_levels"][decision["safety_level"]] += 1
                score = decision["risk_score"]
                result["maximum_recorded_risk_score"] = max(score, result["maximum_recorded_risk_score"] or 0)
                raw_decision = record.get("raw_decision")
                if raw_decision is None:
                    result["raw_decision_missing_or_null"] += 1
                else:
                    result["raw_decisions"][raw_decision["action"]] += 1
                    result["raw_decision_reasons"].update(set(raw_decision["reasons"]))
                result["command_statuses"][command["status"]] += 1
                result["command_lifecycle_statuses"][command.get("command_status", "<missing>")] += 1
                for label, owner, field in [("decision_command_executed", decision, "command_executed"),
                                             ("hardware_command_sent", command, "hardware_command_sent")]:
                    value = str(owner[field]).lower() if field in owner else "<missing>"
                    result["reported_execution_flags"][label][value] += 1
                result["required_approval_decision_records"] += int(decision["requires_human_approval"])
                result["evidence_links"].append({"line": line, "trace_id": trace, "sequence": sequence,
                                                  "evidence_id": evidence["evidence_id"], "frame_index": evidence["frame_index"]})
                if approval_key is not None:
                    status_value = command["approval_status"]
                    if approval_key not in approvals:
                        approvals[approval_key] = {"trace_id": trace, "approval_id": command["approval_id"],
                            "observations": 0, "state_change_count": 0, "repeated_state_records": 0,
                            "duplicate_event_records": 0, "observed_status_counts": Counter(),
                            "status_changes": [], "first_line": line}
                    item = approvals[approval_key]
                    if item["observations"]:
                        if item["last_observed_status"] == status_value:
                            item["repeated_state_records"] += 1
                            result["approvals"]["repeated_state_records"] += 1
                        else:
                            item["status_changes"].append({"line": line, "from": item["last_observed_status"], "to": status_value})
                            item["state_change_count"] += 1
                            result["approvals"]["state_change_count"] += 1
                    item["observations"] += 1
                    item["observed_status_counts"][status_value] += 1
                    item.update(last_observed_status=status_value, last_status_recognized=status_value in APPROVAL_STATUSES, last_line=line)
                    result["approvals"]["observations"] += 1
                if include_records:
                    result["records"].append({"line": line, "record": record})
            stream_stat = os.fstat(stream.fileno())
            unchanged = all(getattr(before, key) == getattr(stream_stat, key)
                            for key in ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns"))
            result["input"].update(sha256=digest.hexdigest(), hash_complete=True, metadata_unchanged_during_read=unchanged)
            if not unchanged:
                diagnostic(None, "error", "input_changed", "", "File metadata changed during reading; hash describes the byte stream, not a stable snapshot.")
    except OSError as error:
        diagnostic(None, "error", "input_io_error", "", str(error))
        result["input"]["partial_sha256"] = digest.hexdigest()
    result["approvals"]["unique_count"] = len(approvals)
    result["approvals"]["items"] = list(approvals.values())
    result["traces"] = [{"trace_id": trace, "included_records": count, "highest_sequence": highwater[trace]}
                        for trace, count in trace_counts.items()]
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Explicit JSONL file; no discovery or directory scanning")
    parser.add_argument("--include-records", action="store_true", help="Include original accepted records, preserving unknown fields")
    parser.add_argument("--max-line-bytes", type=int, default=1024 * 1024)
    args = parser.parse_args(argv)
    if args.max_line_bytes < 1:
        parser.error("--max-line-bytes must be positive")
    result = read_trace(args.path, include_records=args.include_records, max_line_bytes=args.max_line_bytes)
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2, allow_nan=False))
    return 0 if result["valid"] else 2 if any(d["code"] == "input_io_error" for d in result["diagnostics"]) else 1


if __name__ == "__main__":
    sys.exit(main())
