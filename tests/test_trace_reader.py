"""Synthetic parser tests only: no real trace, model, GPU, or core imports."""

import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from trace_reader import read_trace

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "synthetic_trace.jsonl"


def event(sequence=0, trace="synthetic-A", approval=None, status="simulated"):
    evidence_id = "synthetic-evidence-" + str(sequence)
    decision = {"action": "continue_mission", "safety_level": "nominal", "risk_score": 0.1,
                "requires_human_approval": approval is not None, "reasons": ["SYNTHETIC reason"],
                "evidence_id": evidence_id, "command_executed": status == "simulated"}
    command = {"status": status, "command_status": "completed", "hardware_command_sent": False}
    if approval:
        command.update(approval_id=approval[0], approval_status=approval[1])
    return {"_synthetic": True, "fixture_note": "SYNTHETIC parser fixture, not a real run",
            "trace_id": trace, "sequence": sequence,
            "telemetry": {"battery_percent": 50, "altitude_m": 10},
            "evidence": {"evidence_id": evidence_id, "frame_index": sequence,
                         "confidence": 0.9, "obstacle_risk": 0.0, "motion_risk": 0.0},
            "decision": decision, "raw_decision": copy.deepcopy(decision), "command": command}


def encode(*records):
    return b"".join(json.dumps(record).encode() + b"\n" for record in records)


class TraceReaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "trace.jsonl"

    def read(self, data, **kwargs):
        self.path.write_bytes(data)
        before = self.path.stat().st_mtime_ns
        result = read_trace(self.path, **kwargs)
        self.assertEqual(self.path.read_bytes(), data)
        self.assertEqual(self.path.stat().st_mtime_ns, before)
        self.assertEqual(result["input"]["sha256"], hashlib.sha256(data).hexdigest())
        self.assertTrue(result["input"]["hash_complete"])
        return result

    def test_synthetic_fixture_counts_and_scoped_approvals(self):
        raw = FIXTURE.read_bytes()
        result = read_trace(FIXTURE, include_records=True)
        self.assertTrue(result["valid"])
        self.assertEqual(result["input"]["sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(FIXTURE.read_bytes(), raw)
        self.assertEqual(result["counts"]["included_records"], 5)
        self.assertEqual(result["counts"]["duplicate_event_records"], 1)
        self.assertEqual(result["final_decisions"], {"request_human_approval": 4, "continue_mission": 1})
        self.assertEqual(result["raw_decisions"], {"request_human_approval": 3, "hold_and_scan": 1})
        self.assertEqual(result["raw_decision_missing_or_null"], 1)
        self.assertEqual(result["command_statuses"], {"awaiting_human_approval": 3, "simulated": 2})
        self.assertEqual(result["reported_execution_flags"]["hardware_command_sent"], {"false": 5})
        self.assertEqual(result["reported_execution_flags"]["decision_command_executed"], {"false": 3, "true": 2})
        approvals = result["approvals"]
        self.assertEqual(approvals["unique_count"], 2)
        self.assertEqual(approvals["observations"], 4)
        self.assertEqual(approvals["state_change_count"], 1)
        self.assertEqual(approvals["repeated_state_records"], 1)
        self.assertEqual(approvals["duplicate_event_records"], 1)
        self.assertTrue(all(item["record"]["_synthetic"] for item in result["records"]))
        self.assertEqual([link["line"] for link in result["evidence_links"]], [1, 2, 3, 4, 6])
        self.assertEqual(result["required_approval_decision_records"], 4)

    def test_missing_and_null_raw_decision_are_not_inferred(self):
        a, b = event(), event(1)
        a.pop("raw_decision")
        b["raw_decision"] = None
        result = self.read(encode(a, b))
        self.assertEqual(result["raw_decisions"], {})
        self.assertEqual(result["raw_decision_missing_or_null"], 2)

    def test_exact_duplicate_and_conflicting_duplicate_are_separate(self):
        a = event()
        conflict = copy.deepcopy(a)
        conflict["extra"] = "changed unknown field"
        result = self.read(encode(a, a, conflict))
        self.assertFalse(result["valid"])
        self.assertEqual(result["counts"]["included_records"], 1)
        self.assertEqual(result["counts"]["duplicate_event_records"], 1)
        self.assertEqual(result["counts"]["conflicting_event_records"], 1)
        self.assertEqual([(d["line"], d["code"]) for d in result["diagnostics"]],
                         [(2, "duplicate_event"), (3, "conflicting_event")])

    def test_sequence_diagnostics_and_trace_scope(self):
        result = self.read(encode(event(3), event(5), event(4), event(0, trace="synthetic-B")))
        self.assertEqual([(d["line"], d["code"]) for d in result["diagnostics"]],
                         [(1, "sequence_nonzero_start"), (2, "sequence_gap"), (3, "sequence_out_of_order")])
        self.assertEqual(result["counts"]["included_records"], 4)
        self.assertEqual(result["traces"][0]["highest_sequence"], 5)

    def test_required_fields_and_types(self):
        cases = [("trace_id", ""), ("sequence", True), ("sequence", -1),
                 ("telemetry", None), ("evidence", []), ("decision", "bad"), ("command", {})]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                record = event()
                record[field] = value
                result = self.read(encode(record))
                self.assertFalse(result["valid"])
                self.assertEqual(result["counts"]["included_records"], 0)
                self.assertTrue(all(d["line"] == 1 for d in result["diagnostics"]))
        for field in ("confidence", "obstacle_risk", "motion_risk"):
            with self.subTest(field=field):
                record = event()
                record["evidence"][field] = True
                self.assertFalse(self.read(encode(record))["valid"])

    def test_evidence_links_require_final_and_raw_match(self):
        for field in ("decision", "raw_decision"):
            with self.subTest(field=field):
                record = event()
                record[field]["evidence_id"] = "synthetic-wrong"
                result = self.read(encode(record))
                self.assertFalse(result["valid"])
                self.assertIn("evidence_mismatch", {d["code"] for d in result["diagnostics"]})
                self.assertEqual(result["evidence_links"], [])
        result = self.read(encode(event(trace="synthetic-A"), event(trace="synthetic-B")))
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["evidence_links"]), 2)

    def test_corrupt_lines_blank_nonobject_and_truncated_tail(self):
        data = b"\n" + encode(event()) + b"{bad}\n[]\n{\"trace_id\":"
        result = self.read(data)
        self.assertFalse(result["valid"])
        self.assertEqual(result["counts"]["lines"], 5)
        self.assertEqual(result["counts"]["blank_lines"], 1)
        self.assertEqual(result["counts"]["parse_errors"], 2)
        self.assertEqual(result["counts"]["invalid_records"], 1)
        self.assertEqual({d["line"] for d in result["diagnostics"] if d["severity"] == "error"}, {3, 4, 5})

    def test_invalid_utf8_and_crlf_hash_original_bytes(self):
        result = self.read(b"\xff\n" + encode(event()).replace(b"\n", b"\r\n").rstrip(b"\r\n"))
        self.assertFalse(result["valid"])
        self.assertEqual(result["counts"]["included_records"], 1)
        self.assertEqual(result["diagnostics"][0]["line"], 1)

    def test_json_duplicate_keys_and_nonfinite_numbers_are_rejected(self):
        for raw in [b'{"x":NaN}', b'{"x":Infinity}', b'{"x":1e999}',
                    b'{"x":1,"x":2}', b'{"nested":{"x":1,"x":2}}']:
            with self.subTest(raw=raw):
                result = self.read(raw)
                self.assertFalse(result["valid"])
                self.assertEqual(result["diagnostics"][0]["code"], "invalid_json")

    def test_oversized_line_is_skipped_without_truncating_hash(self):
        normal = encode(event())
        limit = len(normal) + 5
        huge = b'{"extra":"' + b'x' * (3 * limit) + b'"}\n'
        result = self.read(huge + normal, max_line_bytes=limit)
        self.assertEqual(result["counts"]["lines"], 2)
        self.assertEqual(result["counts"]["included_records"], 1)
        self.assertEqual(result["diagnostics"][0]["code"], "line_too_long")
        self.assertEqual(result["evidence_links"][0]["line"], 2)

    def test_unknown_fields_and_states_are_retained_not_success(self):
        record = event(approval=("synthetic-approval", "future-status"), status="future-command")
        record["command"]["command_status"] = "future-lifecycle"
        record["extra"] = {"future": [1, 2]}
        record["evidence"]["future_sensor"] = "synthetic-extra"
        record["decision"].pop("command_executed")
        record["command"].pop("hardware_command_sent")
        result = self.read(encode(record), include_records=True)
        self.assertTrue(result["valid"])
        self.assertEqual(result["command_statuses"], {"future-command": 1})
        self.assertEqual(result["command_lifecycle_statuses"], {"future-lifecycle": 1})
        self.assertFalse(result["approvals"]["items"][0]["last_status_recognized"])
        self.assertEqual(result["records"][0]["record"], record)
        self.assertEqual(result["reported_execution_flags"]["hardware_command_sent"], {"<missing>": 1})
        self.assertEqual(result["reported_execution_flags"]["decision_command_executed"], {"<missing>": 1})
        self.assertEqual({d["code"] for d in result["diagnostics"]}, {"unknown_value"})
        self.assertNotIn("success", result)

    def test_approval_changes_include_unknown_states_in_file_order(self):
        records = [event(i, approval=("synthetic-approval", status))
                   for i, status in enumerate(["pending", "future-state", "future-state", "approved"])]
        result = self.read(encode(*records))
        approval = result["approvals"]["items"][0]
        self.assertEqual(approval["state_change_count"], 2)
        self.assertEqual(approval["repeated_state_records"], 1)
        self.assertEqual([c["line"] for c in approval["status_changes"]], [2, 4])
        self.assertEqual(approval["observed_status_counts"]["future-state"], 2)

    def test_missing_approval_metadata_is_not_fabricated(self):
        record = event()
        record["decision"]["requires_human_approval"] = True
        result = self.read(encode(record))
        self.assertEqual(result["approvals"]["unique_count"], 0)
        self.assertEqual(result["required_approval_decision_records"], 1)
        self.assertEqual(result["diagnostics"][0]["code"], "approval_metadata_missing")
        record["command"]["approval_status"] = "approved"
        self.assertFalse(self.read(encode(record))["valid"])

    def test_empty_file_hash_and_no_scan(self):
        result = self.read(b"")
        self.assertEqual(result["counts"]["included_records"], 0)
        self.assertEqual(result["input"]["sha256"], hashlib.sha256(b"").hexdigest())
        (self.path.parent / "unrequested.jsonl").write_bytes(b"malformed")
        self.assertTrue(self.read(encode(event()))["valid"])
        directory = read_trace(self.path.parent)
        self.assertFalse(directory["input"]["hash_complete"])
        self.assertIsNone(directory["input"]["sha256"])

    def test_cli_json_exit_codes_and_explicit_file(self):
        args = [sys.executable, "-B", "-m", "trace_reader"]
        result = subprocess.run(args + [str(FIXTURE)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["valid"])
        self.path.write_bytes(b"broken\n")
        result = subprocess.run(args + [str(self.path)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)["diagnostics"][0]["line"], 1)
        result = subprocess.run(args + [str(self.path.parent / "missing.jsonl")], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stderr)
        report = json.loads(result.stdout)
        self.assertIsNone(report["diagnostics"][0]["line"])
        self.assertFalse(report["input"]["hash_complete"])
        result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("required", result.stderr)

    def test_invalid_line_limit(self):
        for value in (0, -1, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                read_trace(FIXTURE, max_line_bytes=value)


if __name__ == "__main__":
    unittest.main()
