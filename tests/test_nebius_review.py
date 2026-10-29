"""Offline tests only. No API verification or benchmark."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from urllib.error import URLError

from nebius_review import (BASE_URL, MODEL, MockProvider, NebiusProvider,
                           NoRedirect, ReviewError, main, review)

FIXTURE = Path(__file__).parent / "fixtures/synthetic_trace.jsonl"


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(FIXTURE.read_text().splitlines()[0])
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "trace.jsonl"
        self.write(self.record)

    def write(self, record):
        self.path.write_text(json.dumps(record) + "\n")

    def test_mock_loop_hash_and_unchanged_input(self):
        before = self.path.read_bytes()
        result = review(self.path, MockProvider())
        self.assertEqual(result["finding"], "no_recorded_gate_conflict")
        self.assertFalse(result["hardware_action"])
        self.assertEqual(result["input_sha256"], hashlib.sha256(before).hexdigest())
        self.assertEqual(self.path.read_bytes(), before)

    def test_selection_changes_evaluated_check(self):
        self.record["decision"]["command_executed"] = True
        self.write(self.record)
        self.assertEqual(review(self.path, MockProvider())["finding"],
                         "reported_execution_without_recorded_approval")
        provider = Mock()
        provider.complete.return_value = json.dumps({"line": 1,
            "evidence_id": self.record["evidence"]["evidence_id"], "check": "execution_claim"})
        self.assertEqual(review(self.path, provider)["finding"],
                         "execution_reported_not_physically_verified")

    def test_approved_and_missing_flags(self):
        self.record["command"]["approval_status"] = "approved"
        self.record["decision"].pop("command_executed")
        self.record["command"].pop("hardware_command_sent")
        self.write(self.record)
        result = review(self.path, MockProvider())
        self.assertEqual(result["finding"], "no_recorded_gate_conflict")
        self.assertIsNone(result["observation"]["hardware_command_sent"])

    def test_bad_output_rejected(self):
        good = {"line": 1, "evidence_id": self.record["evidence"]["evidence_id"],
                "check": "approval_gate"}
        variants = ["not json", '[]', '{"line":1,"line":2}',
                    json.dumps(dict(good, line=True)), json.dumps(dict(good, line=99)),
                    json.dumps(dict(good, evidence_id="invented")),
                    json.dumps(dict(good, check=[])),
                    json.dumps(dict(good, check="land")), json.dumps(dict(good, command="land"))]
        for value in variants:
            with self.subTest(value=value), self.assertRaises(ReviewError):
                review(self.path, Mock(complete=Mock(return_value=value)))

    def test_invalid_empty_and_large_input_never_call_provider(self):
        for content in ("", "bad json\n", self.path.read_text() + "bad\n"):
            self.path.write_text(content)
            provider = Mock()
            with self.assertRaises(ReviewError):
                review(self.path, provider)
            provider.complete.assert_not_called()
        records = []
        for i in range(33):
            record = copy.deepcopy(self.record)
            record["sequence"] = i
            records.append(json.dumps(record))
        self.path.write_text("\n".join(records))
        with self.assertRaises(ReviewError):
            review(self.path, Mock())

    def test_projection_omits_arbitrary_fields(self):
        self.record["secret_extension"] = "DO_NOT_UPLOAD"
        self.record["decision"]["reasons"] = ["DO_NOT_UPLOAD"]
        self.write(self.record)
        provider = Mock(wraps=MockProvider())
        review(self.path, provider)
        self.assertNotIn("DO_NOT_UPLOAD", str(provider.complete.call_args))

    def test_credentials_and_cost_gate(self):
        with patch.dict("os.environ", {}, clear=True), self.assertRaises(ReviewError):
            NebiusProvider.from_env()
        with self.assertRaises(ReviewError):
            NebiusProvider(api_key="secret", base_url="https://example.com")
        with self.assertRaises(SystemExit):
            main([str(self.path), "--provider", "nebius"])

    @patch("nebius_review.build_opener")
    def test_mocked_http_contract(self, opener):
        response = opener.return_value.open.return_value.__enter__.return_value
        response.status = 200
        response.read.return_value = json.dumps({"model": MODEL, "choices": [{"finish_reason": "stop",
            "message": {"content": "selection text"}}]}).encode()
        self.assertEqual(NebiusProvider(api_key="test-key").complete([]), "selection text")
        request = opener.return_value.open.call_args.args[0]
        self.assertEqual(request.full_url, BASE_URL + "/chat/completions")
        self.assertEqual(request.get_header("Authorization"), "Bearer test-key")
        self.assertEqual(json.loads(request.data)["model"], MODEL)
        self.assertEqual(opener.return_value.open.call_args.kwargs["timeout"], 15)

    @patch("nebius_review.build_opener")
    def test_provider_errors_redacted_without_retry(self, opener):
        opener.return_value.open.side_effect = URLError("test-key sensitive body")
        with self.assertRaises(ReviewError) as caught:
            NebiusProvider(api_key="test-key").complete([])
        self.assertNotIn("test-key", str(caught.exception))
        self.assertEqual(opener.return_value.open.call_count, 1)

    @patch("nebius_review.build_opener")
    def test_truncated_malformed_and_oversized_provider_responses(self, opener):
        response = opener.return_value.open.return_value.__enter__.return_value
        for raw in (b"{}", b"bad", b"x" * 262145,
                    b'{"choices":[{"finish_reason":"length","message":{"content":"{}"}}]}'):
            response.read.return_value = raw
            with self.assertRaises(ReviewError):
                NebiusProvider(api_key="test-key").complete([])

    def test_redirect_refused(self):
        with self.assertRaises(ReviewError):
            NoRedirect().redirect_request(None, None, 302, "", {}, "https://example.com")
