"""Offline model-control serialization; hosted capability remains unverified."""
import io
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from live_smoke import TRACE
from nebius_review import (MODEL, MockProvider, NebiusProvider, ReviewError,
                           TOKEN_FACTORY_BASE_URL, review)


class B4ReasoningTests(unittest.TestCase):
    def messages(self):
        class Capture(MockProvider):
            def complete(self, messages):
                self.messages = messages
                return super().complete(messages)
        provider = Capture()
        review(TRACE, provider)
        return provider.messages

    def test_nvidia_non_thinking_setting_is_serialized_as_false_at_root(self):
        messages = self.messages()
        provider = NebiusProvider(api_key="offline-dummy", base_url=TOKEN_FACTORY_BASE_URL,
                                  reasoning_mode="off")
        request = provider.build_request(messages)
        payload = json.loads(request.data)
        self.assertEqual(payload.pop("chat_template_kwargs"), {"enable_thinking": False})
        default = NebiusProvider(api_key="offline-dummy").build_request(messages)
        self.assertEqual(payload, json.loads(default.data))
        self.assertEqual(payload["messages"], messages)
        self.assertEqual(payload["model"], MODEL)
        self.assertEqual(payload["max_tokens"], 256)
        self.assertNotIn("extra_body", payload)
        self.assertNotIn("reasoning_effort", payload)
        self.assertEqual(request.full_url, TOKEN_FACTORY_BASE_URL + "/chat/completions")

    @patch("nebius_review.build_opener")
    def test_unverified_hosted_setting_is_blocked_before_network(self, opener):
        provider = NebiusProvider(api_key="offline-dummy", reasoning_mode="off")
        with self.assertRaises(ReviewError) as caught:
            provider.complete(self.messages())
        self.assertEqual(caught.exception.code, "reasoning_configuration_unverified")
        self.assertEqual(provider.attempts, 0)
        opener.assert_not_called()

    def test_low_effort_or_wrong_types_cannot_be_silently_substituted(self):
        for mode in ("low", "none", "False", False, None, {}):
            with self.subTest(mode=mode), self.assertRaises(ReviewError):
                NebiusProvider(api_key="offline-dummy", reasoning_mode=mode)

    @patch("nebius_review.build_opener")
    def test_provider_parameter_rejections_have_safe_code_and_no_retry(self, opener):
        for status in (400, 422):
            opener.reset_mock()
            opener.return_value.open.side_effect = HTTPError("https://example.com", status,
                "PRIVATE_SENTINEL", {"Authorization": "PRIVATE_SENTINEL"}, io.BytesIO(b"PRIVATE_SENTINEL"))
            provider = NebiusProvider(api_key="offline-dummy")
            with self.assertRaises(ReviewError) as caught:
                provider.complete(self.messages())
            self.assertEqual(caught.exception.code, "provider_request_rejected")
            self.assertEqual(provider.metadata["http_status"], status)
            self.assertNotIn("PRIVATE_SENTINEL", json.dumps(provider.metadata))
            self.assertNotIn("PRIVATE_SENTINEL", str(caught.exception))
            opener.return_value.open.assert_called_once()
