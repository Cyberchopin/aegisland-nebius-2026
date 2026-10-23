"""Offline isolation and transport contract tests. All records use temporary paths."""
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import live_smoke
import live_smoke_second as second
from nebius_review import TOKEN_FACTORY_BASE_URL


class SecondAttemptTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        self.first_guard = root / "live_attempt_consumed.json"
        self.first_result = root / "live_smoke.json"
        self.first_guard.write_text('{"allowance_consumed":true,"automatic_retry_allowed":false}\n')
        self.first_result.write_text('{"http_status":401}\n')
        self.original = (self.first_guard.read_bytes(), self.first_result.read_bytes())
        self.guard = root / "live_attempt_002_consumed.json"
        self.evidence = root / "live_smoke_002.json"
        for target, value in (("live_smoke.ATTEMPT_RECORD", self.first_guard),
                              ("live_smoke_second.ATTEMPT_RECORD", self.guard),
                              ("live_smoke_second.EVIDENCE_PATH", self.evidence)):
            mock = patch(target, value)
            mock.start()
            self.addCleanup(mock.stop)
        env = patch.dict("os.environ", {"NEBIUS_API_KEY": "offline-dummy-key"}, clear=True)
        env.start()
        self.addCleanup(env.stop)

    def tearDown(self):
        self.assertEqual(self.original, (self.first_guard.read_bytes(), self.first_result.read_bytes()))

    def run_second(self, args=None):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            code = second.main(args if args is not None else ["--allow-paid-api",
                "--owner-authorization", "one-synthetic-request", "--owner-accepts-no-account-cap"])
        self.assertNotIn("offline-dummy-key", stdout.getvalue())
        return code, json.loads(stdout.getvalue())

    def response(self, opener):
        response = opener.return_value.open.return_value.__enter__.return_value
        response.status = 200
        response.headers = {}
        response.read.return_value = json.dumps({"model": live_smoke.MODEL,
            "choices": [{"finish_reason": "stop", "message": {"content": json.dumps({
                "line": 2, "evidence_id": "synthetic-approval_conflict-1", "check": "approval_gate"})}}],
            "usage": {"prompt_tokens": 300, "completion_tokens": 50}}).encode()

    @patch("nebius_review.build_opener")
    def test_second_request_is_independent_and_payload_identical(self, opener):
        self.response(opener)
        code, report = self.run_second()
        self.assertEqual(code, 0)
        self.assertEqual(report["attempt_id"], "b2-smoke-002")
        self.assertEqual(json.loads(self.evidence.read_text()), report)
        self.assertTrue(self.guard.exists())
        request = opener.return_value.open.call_args.args[0]
        self.assertEqual(request.full_url, TOKEN_FACTORY_BASE_URL + "/chat/completions")
        self.assertEqual(hashlib.sha256(request.data).hexdigest(),
                         "e34d598f35ddd27392d8cb0c3126eba41616c0594d5e4297c1bb3087395ae718")
        self.assertEqual(opener.return_value.open.call_args.kwargs["timeout"], 15)
        saved = self.evidence.read_bytes()
        code, report = self.run_second()
        self.assertEqual(code, 1)
        self.assertFalse(report["request_attempted"])
        self.assertEqual(self.evidence.read_bytes(), saved)
        opener.return_value.open.assert_called_once()

    @patch("nebius_review.build_opener")
    def test_consumed_second_guard_blocks_request(self, opener):
        self.guard.write_text('{"allowance_consumed":true}')
        before = self.guard.read_bytes()
        code, report = self.run_second()
        self.assertEqual(code, 1)
        self.assertFalse(report["request_attempted"])
        self.assertEqual(self.guard.read_bytes(), before)
        opener.assert_not_called()

    @patch("nebius_review.build_opener")
    def test_second_preflight_does_not_use_consumed_first_guard(self, opener):
        code, report = self.run_second(["--preflight"])
        self.assertEqual(code, 0)
        self.assertTrue(report["code_checks"]["attempt_allowance_unused"])
        self.assertFalse(self.guard.exists())
        self.assertFalse(self.evidence.exists())
        opener.assert_not_called()

    @patch("nebius_review.build_opener")
    def test_second_timeout_consumes_only_second_guard(self, opener):
        opener.return_value.open.side_effect = TimeoutError("offline timeout")
        code, report = self.run_second()
        self.assertEqual(code, 1)
        self.assertTrue(report["request_attempted"])
        self.assertTrue(self.guard.exists())
        self.assertEqual(json.loads(self.evidence.read_text()), report)
        opener.return_value.open.assert_called_once()

    @patch("nebius_review.build_opener")
    def test_missing_execution_flags_do_not_claim_second_attempt(self, opener):
        code, report = self.run_second([])
        self.assertEqual(code, 2)
        self.assertFalse(self.guard.exists())
        self.assertFalse(self.evidence.exists())
        opener.assert_not_called()

    @patch("nebius_review.build_opener")
    def test_conflicting_endpoint_override_fails_offline(self, opener):
        with patch.dict("os.environ", {"NEBIUS_BASE_URL": live_smoke.BASE_URL}):
            code, report = self.run_second()
        self.assertEqual(code, 1)
        self.assertFalse(report["request_attempted"])
        self.assertFalse(self.guard.exists())
        opener.assert_not_called()

    @patch("nebius_review.build_opener")
    def test_existing_second_evidence_blocks_without_claiming_guard(self, opener):
        self.evidence.write_text('{"preserve":"existing evidence"}\n')
        before = self.evidence.read_bytes()
        code, report = self.run_second()
        self.assertEqual(code, 1)
        self.assertFalse(report["request_attempted"])
        self.assertEqual(self.evidence.read_bytes(), before)
        self.assertFalse(self.guard.exists())
        opener.assert_not_called()

    @patch("nebius_review.build_opener")
    def test_original_command_remains_blocked_by_original_guard(self, opener):
        with redirect_stdout(io.StringIO()):
            code = live_smoke.main(["--allow-paid-api", "--owner-authorization",
                                    "one-synthetic-request", "--owner-accepts-no-account-cap"])
        self.assertEqual(code, 1)
        self.assertFalse(self.guard.exists())
        self.assertFalse(self.evidence.exists())
        opener.assert_not_called()
