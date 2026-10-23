"""Attempt 003 regression tests: synthetic responses and temporary guards only."""
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
import live_smoke_third as third
from nebius_review import MODEL, NebiusProvider, ReviewError, TOKEN_FACTORY_BASE_URL

SECRET = "THIRD_PRIVATE_SENTINEL"


class ThirdAttemptTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        self.prior = {}
        for name in ("live_smoke.json", "live_attempt_consumed.json",
                     "live_smoke_002.json", "live_attempt_002_consumed.json"):
            path = root / name
            path.write_text('{"historical":true}\n')
            self.prior[path] = path.read_bytes()
        self.guard = root / "live_attempt_003_consumed.json"
        self.evidence = root / "live_smoke_003.json"
        for target, value in (("live_smoke.ATTEMPT_RECORD", root / "live_attempt_consumed.json"),
                              ("live_smoke_second.ATTEMPT_RECORD", root / "live_attempt_002_consumed.json"),
                              ("live_smoke_second.EVIDENCE_PATH", root / "live_smoke_002.json"),
                              ("live_smoke_third.ATTEMPT_RECORD", self.guard),
                              ("live_smoke_third.EVIDENCE_PATH", self.evidence)):
            mock = patch(target, value)
            mock.start()
            self.addCleanup(mock.stop)
        env = patch.dict("os.environ", {"NEBIUS_API_KEY": SECRET}, clear=True)
        env.start()
        self.addCleanup(env.stop)

    def tearDown(self):
        for path, value in self.prior.items():
            self.assertEqual(path.read_bytes(), value)

    def call(self, args=None):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            code = third.main(args if args is not None else ["--allow-paid-api",
                "--owner-authorization", "one-synthetic-request", "--owner-accepts-no-account-cap"])
        self.assertNotIn(SECRET, stdout.getvalue())
        return code, json.loads(stdout.getvalue())

    def response(self, opener, finish="stop"):
        response = opener.return_value.open.return_value.__enter__.return_value
        response.status = 200
        response.headers = {"Authorization": SECRET, "Set-Cookie": SECRET}
        selection = {"line": 2, "evidence_id": "synthetic-approval_conflict-1", "check": "approval_gate"}
        response.read.return_value = json.dumps({"model": MODEL,
            "choices": [{"finish_reason": finish, "message": {"content": json.dumps(selection),
                "reasoning_content": SECRET}}],
            "usage": {"prompt_tokens": 324, "completion_tokens": 1024, "total_tokens": 1348,
                "completion_tokens_details": {"reasoning_tokens": 900, "private": SECRET}}}).encode()

    @patch("nebius_review.build_opener")
    def test_third_changes_only_output_budget_and_preserves_contract(self, opener):
        self.response(opener)
        code, report = self.call()
        self.assertEqual(code, 0)
        self.assertEqual(report["attempt_id"], "b3-smoke-003")
        self.assertEqual(report["max_output_tokens"], 1024)
        self.assertEqual(report["finish_reason"], "stop")
        self.assertEqual(report["estimated_cost_usd"], 0.0010188)
        self.assertEqual(report["token_details"]["completion_tokens_details"], {"reasoning_tokens": 900})
        self.assertTrue(report["citation_valid"])
        request = opener.return_value.open.call_args.args[0]
        payload = json.loads(request.data)
        self.assertEqual(payload["max_tokens"], 1024)
        payload["max_tokens"] = 256
        self.assertEqual(hashlib.sha256(json.dumps(payload, allow_nan=False).encode()).hexdigest(),
                         "e34d598f35ddd27392d8cb0c3126eba41616c0594d5e4297c1bb3087395ae718")
        self.assertEqual(request.full_url, TOKEN_FACTORY_BASE_URL + "/chat/completions")
        self.assertEqual(opener.return_value.open.call_args.kwargs["timeout"], 15)
        self.assertEqual(json.loads(self.evidence.read_text()), report)
        saved = self.evidence.read_bytes()
        code, report = self.call()
        self.assertEqual(code, 1)
        self.assertFalse(report["request_attempted"])
        self.assertEqual(saved, self.evidence.read_bytes())
        opener.return_value.open.assert_called_once()

    @patch("nebius_review.build_opener")
    def test_third_preflight_has_independent_guard_and_budget(self, opener):
        code, report = self.call(["--preflight"])
        self.assertEqual(code, 0)
        self.assertTrue(report["code_conditions_pass"])
        self.assertEqual(report["max_output_tokens"], 1024)
        self.assertFalse(self.guard.exists())
        self.assertFalse(self.evidence.exists())
        opener.assert_not_called()

    @patch("nebius_review.build_opener")
    def test_consumed_third_guard_is_never_reset(self, opener):
        self.guard.write_text('{"allowance_consumed":true}\n')
        saved = self.guard.read_bytes()
        code, report = self.call()
        self.assertEqual(code, 1)
        self.assertFalse(report["request_attempted"])
        self.assertEqual(saved, self.guard.read_bytes())
        opener.assert_not_called()

    @patch("nebius_review.build_opener")
    def test_existing_third_evidence_is_never_overwritten(self, opener):
        self.evidence.write_text('{"keep":true}\n')
        saved = self.evidence.read_bytes()
        code, report = self.call()
        self.assertEqual(code, 1)
        self.assertFalse(report["request_attempted"])
        self.assertEqual(saved, self.evidence.read_bytes())
        self.assertFalse(self.guard.exists())
        opener.assert_not_called()

    @patch("nebius_review.build_opener")
    def test_truncated_third_retains_safe_diagnostics(self, opener):
        self.response(opener, "length")
        code, report = self.call()
        self.assertEqual(code, 1)
        self.assertEqual(report["failure_code"], "response_truncated")
        self.assertEqual(report["finish_reason"], "length")
        self.assertTrue(self.guard.exists())
        self.assertNotIn("reasoning_content", self.evidence.read_text())
        opener.return_value.open.assert_called_once()

    @patch("nebius_review.build_opener")
    def test_timeout_is_not_retried(self, opener):
        opener.return_value.open.side_effect = TimeoutError(SECRET)
        code, report = self.call()
        self.assertEqual(code, 1)
        self.assertEqual(report["failure_code"], "provider_unavailable")
        self.assertTrue(self.guard.exists())
        opener.return_value.open.assert_called_once()

    @patch("nebius_review.build_opener")
    def test_no_flags_stays_disabled(self, opener):
        code, report = self.call([])
        self.assertEqual(code, 2)
        self.assertFalse(self.guard.exists())
        self.assertFalse(self.evidence.exists())
        opener.assert_not_called()

    def test_previous_provider_budget_remains_256_and_invalid_limits_rejected(self):
        self.assertEqual(NebiusProvider(api_key=SECRET).max_output_tokens, 256)
        for value in (True, 0, 1025, 2048, "1024"):
            with self.assertRaises(ReviewError):
                NebiusProvider(api_key=SECRET, max_output_tokens=value)
