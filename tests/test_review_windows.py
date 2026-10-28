import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock

from model_evaluation import BaselineProvider
from nebius_review import ReviewError, review
from scripts.build_review_workbench import embedded_json, public_provenance

ROOT = Path(__file__).resolve().parents[1]


class WindowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "long.jsonl"
        original = json.loads((ROOT / "evaluation/traces/approval_conflict.jsonl").read_text().splitlines()[0])
        rows = []
        for sequence in range(40):
            row = copy.deepcopy(original)
            row["sequence"] = sequence
            row["evidence"]["frame_index"] = sequence
            row["evidence"]["evidence_id"] = row["decision"]["evidence_id"] = f"test-{sequence}"
            rows.append(json.dumps(row))
        self.path.write_text("\n".join(rows) + "\n", encoding="utf-8")

    def test_window_retains_original_line_and_full_hash(self):
        import hashlib
        result = review(self.path, BaselineProvider(), line_window=(33, 40))
        self.assertEqual(result["selection"]["line"], 33)
        self.assertEqual(result["selection"]["evidence_id"], "test-32")
        self.assertEqual(result["input_sha256"], hashlib.sha256(self.path.read_bytes()).hexdigest())

    def test_unbounded_long_trace_and_bad_windows_never_call_provider(self):
        for window in (None, (0, 3), (1, 33), (True, 4), (1, 41), (4, 3), [1, 4], (1,)):
            provider = Mock()
            with self.subTest(window=window), self.assertRaises(ReviewError):
                review(self.path, provider, line_window=window)
            provider.complete.assert_not_called()

    def test_outside_window_citation_rejected(self):
        provider = Mock(complete=Mock(return_value=json.dumps({
            "line": 1, "evidence_id": "test-0", "check": "approval_gate"})))
        with self.assertRaises(ReviewError) as caught:
            review(self.path, provider, line_window=(33, 40))
        self.assertEqual(caught.exception.code, "citation_mismatch")
        packet = json.loads(provider.complete.call_args.args[0][1]["content"])
        self.assertEqual([event["line"] for event in packet], list(range(33, 41)))

    def test_invalid_record_outside_window_blocks_review(self):
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write("{broken}\n")
        provider = Mock()
        with self.assertRaises(ReviewError) as caught:
            review(self.path, provider, line_window=(1, 2))
        self.assertEqual(caught.exception.code, "trace_invalid")
        provider.complete.assert_not_called()

    def test_embedded_record_cannot_end_json_element(self):
        original = {"reason": '</script><img src=x onerror="alert(1)"> & 中文'}
        encoded = embedded_json(original)
        self.assertNotIn("<", encoded)
        self.assertNotIn(">", encoded)
        self.assertEqual(json.loads(encoded), original)

    def test_public_provenance_omits_filesystem_environment_and_commands(self):
        record = {"core_commit": "a" * 40, "status": "PASS",
                  "validation": {"trace_events": 2, "decoded_video_frames": 2,
                                 "all_commands_simulation_only": True},
                  "sha256": {"trace.jsonl": "b" * 64},
                  "cwd": "/home/PRIVATE_SENTINEL/project",
                  "command": ["PRIVATE_SENTINEL"],
                  "environment_overrides": {"PRIVATE_SENTINEL": "PRIVATE_SENTINEL"}}
        result = public_provenance(record, name="nominal", original_sha256="c" * 64,
                                   original_blob="d" * 40)
        self.assertNotIn("PRIVATE_SENTINEL", json.dumps(result))
        self.assertNotIn("cwd", result)
        self.assertNotIn("command", result)
        self.assertNotIn("environment_overrides", result)
        self.assertEqual(result["sha256"], record["sha256"])


class ReplayRangeTests(unittest.TestCase):
    def test_browser_range_requests_return_exact_bytes(self):
        from functools import partial
        from http.client import HTTPConnection
        from http.server import ThreadingHTTPServer
        from threading import Thread
        from scripts.serve_review_workbench import ReplayHandler
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "replay.mp4").write_bytes(b"0123456789")
            server = ThreadingHTTPServer(("127.0.0.1", 0), partial(ReplayHandler, directory=directory))
            worker = Thread(target=server.serve_forever, daemon=True)
            worker.start()
            try:
                for header, status, expected in (("bytes=3-6", 206, b"3456"),
                                                  ("bytes=8-", 206, b"89"),
                                                  ("bytes=99-", 416, b"")):
                    connection = HTTPConnection("127.0.0.1", server.server_port, timeout=5)
                    try:
                        connection.request("GET", "/replay.mp4", headers={"Range": header})
                        response = connection.getresponse()
                        self.assertEqual(response.status, status)
                        self.assertEqual(response.read(), expected)
                    finally:
                        connection.close()
            finally:
                server.shutdown()
                server.server_close()
                worker.join(timeout=5)
