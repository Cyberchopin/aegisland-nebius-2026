"""Synthetic, offline B2 verification; all network boundaries are mocked."""
from contextlib import redirect_stdout, redirect_stderr
import io
import json
import tempfile
from pathlib import Path
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError

import live_smoke
from model_evaluation import BaselineProvider, MANIFEST, evaluate, safe_review
from nebius_review import NebiusProvider, ReviewError, review
from trace_reader import read_trace

TRACE = live_smoke.TRACE
SECRET = "SENTINEL_PRIVATE_TOKEN"


class EvaluationTests(unittest.TestCase):
    def test_all_scenarios_valid_and_synthetic(self):
        manifest = json.loads(MANIFEST.read_text())
        self.assertGreaterEqual(len(manifest["scenarios"]), 5)
        for scenario in manifest["scenarios"]:
            summary = read_trace(MANIFEST.parent / scenario["trace"], include_records=True)
            self.assertTrue(summary["valid"])
            self.assertTrue(all(x["record"]["_synthetic"] for x in summary["records"]))

    def test_repeatable_baseline_comparison(self):
        first = evaluate()
        self.assertEqual(first, evaluate())
        self.assertEqual(first["baseline_matches"], 6)
        self.assertEqual(first["candidate_matches"], 1)
        self.assertFalse(first["actual_nvidia_inference"])
        self.assertEqual(first["live_api_calls"], 0)

    def test_timeout_and_arbitrary_provider_error_fall_back(self):
        for error in (TimeoutError(SECRET), RuntimeError(SECRET), ReviewError(SECRET)):
            provider = Mock(complete=Mock(side_effect=error))
            result = safe_review(TRACE, provider)
            self.assertEqual(result["status"], "fallback")
            self.assertEqual(result["source"], "deterministic_baseline")
            self.assertEqual(result["result"]["finding"], "reported_execution_without_recorded_approval")
            self.assertNotIn(SECRET, json.dumps(result))
            provider.complete.assert_called_once()

    def test_invalid_selection_falls_back_never_accepted(self):
        for content in ('{"line":2,"evidence_id":"invented","check":"approval_gate"}',
                        '{"line":2,"evidence_id":"synthetic-approval_conflict-1","check":"land"}',
                        "I refuse this request", "{broken"):
            result = safe_review(TRACE, Mock(complete=Mock(return_value=content)))
            self.assertEqual(result["status"], "fallback")
            self.assertFalse(result["result"]["hardware_action"])

    def test_invalid_trace_unavailable_no_candidate_call(self):
        candidate = Mock()
        result = safe_review(Path("nonexistent-b2-trace.jsonl"), candidate)
        self.assertEqual(result["status"], "unavailable")
        self.assertIsNone(result["result"])
        candidate.complete.assert_not_called()


class SmokeTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.attempt_path = Path(temp.name) / "consumed.json"
        attempt_patch = patch("live_smoke.ATTEMPT_RECORD", self.attempt_path)
        attempt_patch.start()
        self.addCleanup(attempt_patch.stop)


    @patch("nebius_review.build_opener")
    def test_preflight_missing_credentials_is_offline(self, opener):
        with patch.dict("os.environ", {}, clear=True):
            code, report = self.call(["--preflight"])
        self.assertEqual(code, 1)
        self.assertTrue(report["trace_valid"])
        self.assertFalse(report["credential_and_configuration_valid"])
        self.assertFalse(report["request_attempted"])
        opener.assert_not_called()

    @patch("nebius_review.build_opener")
    def test_preflight_with_key_and_live_flags_still_offline(self, opener):
        with patch.dict("os.environ", {"NEBIUS_API_KEY": SECRET}, clear=True):
            code, report = self.call(["--preflight", "--allow-paid-api",
                                      "--owner-authorization", "one-synthetic-request"])
        self.assertEqual(code, 0)
        self.assertTrue(report["ready_for_authorized_attempt"])
        self.assertEqual(report["account_access_quota_pricing"], "not_verified")
        self.assertFalse(report["request_attempted"])
        opener.assert_not_called()

    @patch("nebius_review.build_opener")
    def test_preflight_invalid_endpoint_not_echoed(self, opener):
        with patch.dict("os.environ", {"NEBIUS_API_KEY": SECRET,
                                       "NEBIUS_BASE_URL": "https://example.com/" + SECRET}, clear=True):
            code, report = self.call(["--preflight"])
        self.assertEqual(code, 1)
        self.assertFalse(report["credential_and_configuration_valid"])
        opener.assert_not_called()

    def call(self, args, billing_flag="--account-cap-confirmed"):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = live_smoke.main(args + [billing_flag])
        self.assertEqual(stderr.getvalue(), "")
        self.assertNotIn(SECRET, stdout.getvalue())
        return code, json.loads(stdout.getvalue())

    @patch("live_smoke.NebiusProvider.from_env")
    def test_disabled_even_with_only_one_gate(self, factory):
        for args in ([], ["--allow-paid-api"], ["--owner-authorization", "one-synthetic-request"]):
            code, report = self.call(args)
            self.assertEqual(code, 2)
            self.assertFalse(report["request_attempted"])
        factory.assert_not_called()

    def test_missing_credentials_no_network(self):
        with patch.dict("os.environ", {}, clear=True), patch("nebius_review.build_opener") as opener:
            code, report = self.call(["--allow-paid-api", "--owner-authorization", "one-synthetic-request"])
        self.assertEqual(code, 1)
        self.assertFalse(report["request_attempted"])
        opener.assert_not_called()

    @patch("nebius_review.build_opener")
    def test_mocked_smoke_success_output_allowlist(self, opener):
        selection = {"line": 2, "evidence_id": "synthetic-approval_conflict-1", "check": "approval_gate"}
        data = {"model": live_smoke.MODEL, "choices": [{"finish_reason": "stop", "message": {"content": json.dumps(selection)}}],
                "usage": {"prompt_tokens": 100, "completion_tokens": 30, "total_tokens": 130,
                          "secret": SECRET}, "secret": SECRET}
        response = opener.return_value.open.return_value.__enter__.return_value
        response.read.return_value = json.dumps(data).encode()
        response.status = 200
        response.headers = {"Authorization": SECRET, "Set-Cookie": SECRET, "x-request-id": "req-123"}
        with patch.dict("os.environ", {"NEBIUS_API_KEY": SECRET}, clear=True):
            code, report = self.call(["--allow-paid-api", "--owner-authorization", "one-synthetic-request"])
        self.assertEqual(code, 0)
        self.assertTrue(report["matches_synthetic_expectation"])
        self.assertEqual(report["usage"], {"prompt_tokens": 100, "completion_tokens": 30, "total_tokens": 130})
        self.assertNotIn("selection", report)
        self.assertEqual(report["response_model"], live_smoke.MODEL)
        self.assertEqual(report["http_status"], 200)
        self.assertEqual(report["estimated_cost_usd"], 0.000057)
        self.assertGreaterEqual(report["elapsed_latency_ms"], 0)
        self.assertEqual(len(report["provider_request_id_sha256"]), 64)
        request = opener.return_value.open.call_args.args[0]
        self.assertEqual(json.loads(request.data)["max_tokens"], 256)
        opener.return_value.open.assert_called_once()
        code, second = self.call(["--allow-paid-api", "--owner-authorization", "one-synthetic-request"])
        self.assertEqual(code, 1)
        self.assertFalse(second["request_attempted"])
        opener.return_value.open.assert_called_once()

    @patch("nebius_review.build_opener")
    def test_unconfirmed_billing_cap_never_calls_provider(self, opener):
        with redirect_stdout(io.StringIO()):
            code = live_smoke.main(["--allow-paid-api", "--owner-authorization", "one-synthetic-request"])
        self.assertEqual(code, 2)
        opener.assert_not_called()

    @patch("nebius_review.build_opener")
    def test_billing_flags_mutually_exclusive(self, opener):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
            live_smoke.main(["--account-cap-confirmed", "--owner-accepts-no-account-cap"])
        self.assertEqual(caught.exception.code, 2)
        self.assertFalse(self.attempt_path.exists())
        opener.assert_not_called()

    @patch("nebius_review.build_opener")
    def test_no_cap_acceptance_still_requires_credentials_and_other_gates(self, opener):
        flag = "--owner-accepts-no-account-cap"
        for args in ([], ["--allow-paid-api"], ["--owner-authorization", "one-synthetic-request"]):
            code, report = self.call(args, flag)
            self.assertEqual(code, 2)
            self.assertFalse(report["request_attempted"])
        with patch.dict("os.environ", {}, clear=True):
            code, report = self.call(["--allow-paid-api", "--owner-authorization", "one-synthetic-request"], flag)
        self.assertEqual(code, 1)
        self.assertEqual(report["billing_authorization"], "owner_accepts_no_account_cap")
        self.assertFalse(report["request_attempted"])
        self.assertFalse(self.attempt_path.exists())
        opener.assert_not_called()

    @patch("nebius_review.build_opener")
    def test_no_cap_mocked_request_preserves_limits_and_persistent_guard(self, opener):
        selection = {"line": 2, "evidence_id": "synthetic-approval_conflict-1", "check": "approval_gate"}
        response = opener.return_value.open.return_value.__enter__.return_value
        response.status = 200
        response.headers = {}
        response.read.return_value = json.dumps({"model": live_smoke.MODEL, "choices": [
            {"finish_reason": "stop", "message": {"content": json.dumps(selection)}}]}).encode()
        args = ["--allow-paid-api", "--owner-authorization", "one-synthetic-request"]
        with patch.dict("os.environ", {"NEBIUS_API_KEY": SECRET}, clear=True):
            code, report = self.call(args, "--owner-accepts-no-account-cap")
            self.assertEqual(code, 0)
            self.assertEqual(report["billing_authorization"], "owner_accepts_no_account_cap")
            request = opener.return_value.open.call_args.args[0]
            self.assertEqual(json.loads(request.data)["max_tokens"], 256)
            self.assertEqual(opener.return_value.open.call_args.kwargs["timeout"], 15)
            self.assertTrue(self.attempt_path.exists())
            code, report = self.call(args, "--owner-accepts-no-account-cap")
            self.assertEqual(code, 1)
            self.assertFalse(report["request_attempted"])
        opener.return_value.open.assert_called_once()

    @patch("nebius_review.build_opener")
    def test_provider_instance_cannot_retry_after_timeout(self, opener):
        opener.return_value.open.side_effect = TimeoutError(SECRET)
        provider = NebiusProvider(api_key=SECRET)
        for _ in range(2):
            with self.assertRaises(ReviewError):
                provider.complete([])
        opener.return_value.open.assert_called_once()

    def test_preflight_verifies_code_limits(self):
        report = live_smoke.preflight()
        self.assertTrue(report["code_conditions_pass"])
        self.assertEqual(report["max_output_tokens"], 256)
        self.assertEqual(report["timeout_seconds"], 15)
        self.assertFalse(report["billing_cap_verified"])
        self.assertFalse(report["live_ready"])

    @patch("nebius_review.build_opener")
    def test_unknown_response_model_never_verified(self, opener):
        selection = {"line": 2, "evidence_id": "synthetic-approval_conflict-1", "check": "approval_gate"}
        response = opener.return_value.open.return_value.__enter__.return_value
        response.read.return_value = json.dumps({"model": SECRET, "choices": [
            {"finish_reason": "stop", "message": {"content": json.dumps(selection)}}]}).encode()
        with patch.dict("os.environ", {"NEBIUS_API_KEY": SECRET}, clear=True):
            code, report = self.call(["--allow-paid-api", "--owner-authorization", "one-synthetic-request"])
        self.assertEqual(code, 1)
        self.assertEqual(report["status"], "not_verified")
        self.assertIsNone(report["response_model"])

    @patch("nebius_review.build_opener")
    def test_timeout_http_error_refusal_and_malformed_redacted(self, opener):
        args = ["--allow-paid-api", "--owner-authorization", "one-synthetic-request"]
        with patch.dict("os.environ", {"NEBIUS_API_KEY": SECRET}, clear=True):
            for error in (TimeoutError(SECRET), HTTPError("https://example.com", 401, SECRET,
                                                        {"Set-Cookie": SECRET}, io.BytesIO(SECRET.encode()))):
                self.attempt_path.unlink(missing_ok=True)
                opener.return_value.open.side_effect = error
                code, report = self.call(args)
                self.assertEqual(code, 1)
                self.assertTrue(report["request_attempted"])
            opener.return_value.open.side_effect = None
            response = opener.return_value.open.return_value.__enter__.return_value
            for raw in (SECRET.encode(), json.dumps({"choices": [{"finish_reason": "stop",
                        "message": {"refusal": SECRET, "content": "{}"}}]}).encode()):
                self.attempt_path.unlink(missing_ok=True)
                response.read.return_value = raw
                code, report = self.call(args)
                self.assertEqual(code, 1)
                self.assertEqual(report["status"], "not_verified")

    @patch("nebius_review.build_opener")
    def test_explicit_model_refusal_rejected(self, opener):
        response = opener.return_value.open.return_value.__enter__.return_value
        response.read.return_value = json.dumps({"choices": [{"finish_reason": "stop",
                                  "message": {"refusal": SECRET, "content": "{}"}}]}).encode()
        with self.assertRaises(ReviewError) as caught:
            NebiusProvider(api_key=SECRET).complete([])
        self.assertEqual(caught.exception.code, "model_refusal")
        self.assertNotIn(SECRET, str(caught.exception))
