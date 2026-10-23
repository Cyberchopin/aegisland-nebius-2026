"""Synthetic B3 parser and sanitized provider diagnostics; no network requests."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import live_smoke
from nebius_review import MODEL, NebiusProvider, ReviewError, review, safe_failure_code

SECRET = "PRIVATE_SENTINEL_DO_NOT_RETAIN"


class B3DiagnosticsTests(unittest.TestCase):
    def envelope(self, *, finish="stop", content="{}", usage=None):
        return {"model": MODEL, "choices": [{"finish_reason": finish,
                "message": {"content": content, "reasoning_content": SECRET}}],
                "usage": usage or {"prompt_tokens": 324, "completion_tokens": 256,
                                   "total_tokens": 580}}

    def mock_response(self, opener, data):
        response = opener.return_value.open.return_value.__enter__.return_value
        response.status = 200
        response.headers = {}
        response.read.return_value = json.dumps(data).encode()

    def test_synthetic_parser_fixtures(self):
        fixture = Path(__file__).parent / "fixtures/review_outputs_b3.json"
        for case in json.loads(fixture.read_text())["cases"]:
            with self.subTest(case=case["id"]):
                provider = Mock(complete=Mock(return_value=case["content"]))
                if case["expected"] == "valid":
                    result = review(live_smoke.TRACE, provider)
                    self.assertEqual(result["selection"]["line"], 2)
                    self.assertEqual(result["finding"], "reported_execution_without_recorded_approval")
                else:
                    with self.assertRaises(ReviewError) as caught:
                        review(live_smoke.TRACE, provider)
                    self.assertEqual(caught.exception.code, case["expected"])

    @patch("nebius_review.build_opener")
    def test_length_rejected_even_when_json_is_valid(self, opener):
        self.mock_response(opener, self.envelope(finish="length"))
        provider = NebiusProvider(api_key=SECRET)
        with self.assertRaises(ReviewError) as caught:
            provider.complete([])
        self.assertEqual(caught.exception.code, "response_truncated")
        self.assertEqual(provider.metadata["finish_reason"], "length")
        self.assertEqual(provider.usage["completion_tokens"], 256)
        self.assertNotIn(SECRET, json.dumps(provider.metadata))
        opener.return_value.open.assert_called_once()

    @patch("nebius_review.build_opener")
    def test_usage_details_allowlist_rejects_strings_booleans_and_extensions(self, opener):
        usage = {"prompt_tokens": 324, "completion_tokens": 256, "total_tokens": 580,
                 "prompt_tokens_details": {"cached_tokens": 12, "audio_tokens": True, "private": SECRET},
                 "completion_tokens_details": {"reasoning_tokens": 230, "audio_tokens": SECRET,
                    "accepted_prediction_tokens": -1, "rejected_prediction_tokens": 0, "private": SECRET}}
        self.mock_response(opener, self.envelope(usage=usage))
        provider = NebiusProvider(api_key=SECRET)
        provider.complete([])
        self.assertEqual(provider.metadata["token_details"], {
            "prompt_tokens_details": {"cached_tokens": 12},
            "completion_tokens_details": {"reasoning_tokens": 230, "rejected_prediction_tokens": 0}})
        self.assertNotIn(SECRET, json.dumps(provider.metadata))

    @patch("nebius_review.build_opener")
    def test_unknown_finish_reason_is_redacted(self, opener):
        self.mock_response(opener, self.envelope(finish=SECRET))
        provider = NebiusProvider(api_key=SECRET)
        with self.assertRaises(ReviewError) as caught:
            provider.complete([])
        self.assertEqual(caught.exception.code, "response_not_complete")
        self.assertEqual(provider.metadata["finish_reason"], "unrecognized")
        self.assertNotIn(SECRET, json.dumps(provider.metadata))

    @patch("nebius_review.build_opener")
    def test_refusal_retains_finish_and_counts_without_text(self, opener):
        data = self.envelope(finish="content_filter")
        data["choices"][0]["message"]["refusal"] = SECRET
        self.mock_response(opener, data)
        provider = NebiusProvider(api_key=SECRET)
        with self.assertRaises(ReviewError) as caught:
            provider.complete([])
        self.assertEqual(caught.exception.code, "model_refusal")
        self.assertEqual(provider.metadata["finish_reason"], "content_filter")
        self.assertEqual(provider.usage["total_tokens"], 580)

    def test_unknown_failure_code_is_never_logged(self):
        self.assertEqual(safe_failure_code(ReviewError(SECRET, SECRET)), "review_failed")

    @patch("nebius_review.build_opener")
    def test_smoke_failure_records_safe_code_without_new_real_guard(self, opener):
        self.mock_response(opener, self.envelope(finish="length"))
        with tempfile.TemporaryDirectory() as directory, patch.dict("os.environ", {"NEBIUS_API_KEY": SECRET}, clear=True):
            root = Path(directory)
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = live_smoke.main(["--allow-paid-api", "--owner-authorization", "one-synthetic-request",
                    "--owner-accepts-no-account-cap"], attempt_record=root / "synthetic_guard.json")
            result = json.loads(stdout.getvalue())
        self.assertEqual(code, 1)
        self.assertEqual(result["failure_code"], "response_truncated")
        self.assertEqual(result["finish_reason"], "length")
        self.assertNotIn(SECRET, stdout.getvalue())
