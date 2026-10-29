"""Attempt 004 synthetic transport fixtures only. Never real NVIDIA output."""
from contextlib import redirect_stdout, redirect_stderr
import copy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

import nebius_review as n

SECRET = 'OFFLINE_PRIVATE_SENTINEL'
REQUEST_ID = 'OFFLINE_REQUEST_ID_SENTINEL'
SELECTION = {'line': 39, 'evidence_id': 'c71390b01d39', 'check': 'approval_gate'}


class Attempt004Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.serial = 0
        self.guard = self.root / 'guard.json'
        def start(patcher):
            value = patcher.start()
            self.addCleanup(patcher.stop)
            return value
        start(patch('nebius_review.ATTEMPT004_GUARD', self.guard))
        start(patch.dict('os.environ', {'NEBIUS_API_KEY': SECRET}, clear=True))
        self.external_attempts = []
        def deny(*args, **kwargs):
            self.external_attempts.append(True)
            raise AssertionError('No sockets are permitted in Attempt 004 unit tests')
        for target in ('socket.create_connection', 'socket.socket.connect', 'socket.getaddrinfo'):
            start(patch(target, side_effect=deny))
        self.opener = start(patch('nebius_review.build_opener'))
        self.response = self.opener.return_value.open.return_value.__enter__.return_value
        self.response.status = 200
        self.response.headers = {'x-request-id': REQUEST_ID, 'Authorization': SECRET,
                                 'Set-Cookie': SECRET, 'sensitive-account': SECRET}
        self.envelope = {'id': REQUEST_ID, 'model': n.MODEL, 'choices': [{'finish_reason': 'stop',
            'message': {'content': json.dumps(SELECTION), 'reasoning_content': SECRET}}],
            'usage': {'prompt_tokens': 400, 'completion_tokens': 40, 'total_tokens': 440,
                      'completion_tokens_details': {'reasoning_tokens': 0, 'sensitive': SECRET}}}
        self.response.read.side_effect = lambda *_: json.dumps(self.envelope).encode()

    def tearDown(self):
        self.assertEqual(self.external_attempts, [])
        for path in self.root.rglob('*.json'):
            text = path.read_text()
            self.assertNotIn(SECRET, text)
            self.assertNotIn(REQUEST_ID, text)
            self.assertNotIn(str(self.root), text)

    def args(self, output=None):
        self.serial += 1
        return [str(n.ATTEMPT004_TRACE), '--provider', 'nebius', '--allow-paid-api',
                '--reasoning-mode', 'off', '--line-window', '38', '39',
                '--output-dir', str(output or self.root / f'output-{self.serial}'),
                '--owner-authorization', 'attempt-004', '--owner-accepts-no-account-cap']

    def call(self, args=None):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = n.main(self.args() if args is None else args)
        self.assertNotIn(SECRET, stdout.getvalue() + stderr.getvalue())
        self.assertNotIn(REQUEST_ID, stdout.getvalue() + stderr.getvalue())
        self.assertNotIn(str(self.root), stdout.getvalue() + stderr.getvalue())
        return code, json.loads(stdout.getvalue() or stderr.getvalue())

    def independent_case(self):
        self.serial += 1
        self.guard = self.root / f'guard-case-{self.serial}.json'
        n.ATTEMPT004_GUARD = self.guard
        self.opener.reset_mock()
        self.opener.return_value.open.side_effect = None

    def test_exact_off_payload_and_default_serialization_unchanged(self):
        _, events, messages, digest, size = n.prepare_attempt004(n.ATTEMPT004_TRACE, (38, 39))
        self.assertEqual([(e['line'], e['evidence_id']) for e in events],
                         [(38, '11d9fc7b7295'), (39, 'c71390b01d39')])
        off = n.NebiusProvider(api_key=SECRET, base_url=n.TOKEN_FACTORY_BASE_URL,
                              reasoning_mode='off').build_request(messages)
        self.assertEqual(hashlib.sha256(off.data).hexdigest(), digest)
        self.assertEqual(digest, n.ATTEMPT004_PAYLOAD_SHA256)
        self.assertEqual(size, 1327)
        body = json.loads(off.data)
        self.assertEqual(body.pop('chat_template_kwargs'), {'enable_thinking': False})
        default = n.NebiusProvider(api_key=SECRET).build_request(messages)
        self.assertEqual(body, json.loads(default.data))
        self.assertEqual(default.full_url, n.BASE_URL + '/chat/completions')
        self.assertNotIn('extra_body', body)
        self.opener.assert_not_called()

    def test_default_mock_never_calls_provider_even_with_environment_key(self):
        code, result = self.call([str(n.ROOT / 'evaluation/traces/approval_conflict.jsonl')])
        self.assertEqual(code, 0)
        self.assertEqual(result['provider'], 'mock')
        self.assertIsNone(result['model'])
        self.assertFalse(result['hardware_action'])
        self.opener.assert_not_called()
        self.assertFalse(self.guard.exists())

    def test_every_live_gate_is_mandatory(self):
        for omitted in ('--allow-paid-api', '--reasoning-mode', '--output-dir',
                        '--line-window', '--owner-authorization', '--owner-accepts-no-account-cap'):
            args = self.args()
            i = args.index(omitted)
            count = 3 if omitted == '--line-window' else 2 if omitted in (
                '--reasoning-mode', '--output-dir', '--owner-authorization') else 1
            del args[i:i + count]
            with self.subTest(omitted=omitted), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                n.main(args)
        self.opener.assert_not_called()
        self.assertFalse(self.guard.exists())

    def test_successful_mocked_receipt_and_http_contract(self):
        self.guard = self.root / 'guard-state' / 'attempt_consumed.json'
        n.ATTEMPT004_GUARD = self.guard
        args = self.args()
        out = Path(args[args.index('--output-dir') + 1])
        code, result = self.call(args)
        self.assertEqual(code, 0)
        self.assertEqual(result, json.loads((out / 'receipt.json').read_text()))
        self.assertTrue(result['citation_valid'])
        self.assertEqual(result['selection'], SELECTION)
        self.assertEqual(result['input_trace_sha256'], n.ATTEMPT004_TRACE_SHA256)
        self.assertEqual(result['request_payload_sha256'], n.ATTEMPT004_PAYLOAD_SHA256)
        self.assertEqual(result['response_model'], n.MODEL)
        self.assertEqual(result['finish_reason'], 'stop')
        self.assertEqual(result['http_status'], 200)
        self.assertEqual(result['usage']['total_tokens'], 440)
        self.assertEqual(result['token_details']['completion_tokens_details'], {'reasoning_tokens': 0})
        self.assertEqual(result['provider_request_id_sha256'], hashlib.sha256(REQUEST_ID.encode()).hexdigest())
        self.assertIsNotNone(result['finding'])
        self.assertGreaterEqual(result['elapsed_latency_ms'], 0)
        self.assertFalse(result['hardware_action'])
        self.assertEqual(result['request_attempts'], 1)
        self.assertEqual(result['reasoning_configuration_support'], 'unconfirmed')
        request = self.opener.return_value.open.call_args.args[0]
        self.assertEqual(request.full_url, n.TOKEN_FACTORY_BASE_URL + '/chat/completions')
        self.assertEqual(request.get_header('Authorization'), 'Bearer ' + SECRET)
        body = json.loads(request.data)
        self.assertEqual(body['chat_template_kwargs'], {'enable_thinking': False})
        self.assertEqual(body['max_tokens'], 256)
        self.assertEqual(self.opener.return_value.open.call_args.kwargs, {'timeout': 15})
        self.assertIsInstance(self.opener.call_args.args[0], n.NoRedirect)
        self.opener.return_value.open.assert_called_once()

    def test_guard_prevents_rerun_with_a_different_output_directory(self):
        code, _ = self.call()
        self.assertEqual(code, 0)
        saved = self.guard.read_bytes()
        code, result = self.call()
        self.assertEqual(code, 1)
        self.assertEqual(result['status'], 'not_verified')
        self.assertEqual(saved, self.guard.read_bytes())
        self.opener.return_value.open.assert_called_once()

    def test_provider_instance_hard_limit_after_success_and_failure(self):
        for error in (None, TimeoutError(SECRET)):
            self.independent_case()
            self.opener.return_value.open.side_effect = error
            provider = n.NebiusProvider(api_key=SECRET, reasoning_mode='off',
                                       allow_unverified_reasoning=True)
            if error is None:
                provider.complete([])
            else:
                with self.assertRaises(n.ReviewError): provider.complete([])
            with self.assertRaises(n.ReviewError): provider.complete([])
            self.assertEqual(provider.attempts, 1)
            self.opener.return_value.open.assert_called_once()

    def test_all_error_statuses_stop_without_retry_or_parameter_removal(self):
        for status in (400, 401, 403, 422, 429, 500, 502, 503, 504):
            with self.subTest(status=status):
                self.independent_case()
                self.opener.return_value.open.side_effect = HTTPError('https://private.example/' + SECRET,
                    status, SECRET, {'x-request-id': REQUEST_ID, 'Authorization': SECRET}, io.BytesIO(SECRET.encode()))
                code, result = self.call()
                self.assertEqual(code, 1)
                self.assertEqual(result['http_status'], status)
                self.assertTrue(result['request_attempted'])
                self.assertTrue(self.guard.exists())
                self.assertFalse(result['citation_valid'])
                self.assertIsNone(result['selection'])
                self.opener.return_value.open.assert_called_once()
                body = json.loads(self.opener.return_value.open.call_args.args[0].data)
                self.assertEqual(body['chat_template_kwargs'], {'enable_thinking': False})
                guard_before = self.guard.read_bytes()
                self.call()
                self.opener.return_value.open.assert_called_once()
                self.assertEqual(guard_before, self.guard.read_bytes())

    def test_timeout_url_error_and_generic_transport_failure_stop(self):
        for error in (TimeoutError(SECRET), URLError(SECRET), OSError(SECRET)):
            with self.subTest(kind=type(error).__name__):
                self.independent_case()
                self.opener.return_value.open.side_effect = error
                code, result = self.call()
                self.assertEqual(code, 1)
                self.assertEqual(result['failure_code'], 'provider_unavailable')
                self.assertIsNone(result['http_status'])
                self.assertTrue(self.guard.exists())
                self.opener.return_value.open.assert_called_once()

    def test_mismatched_or_missing_model_is_rejected_and_redacted(self):
        for model in (SECRET, None):
            self.independent_case()
            self.envelope['model'] = model
            code, result = self.call()
            self.assertEqual(code, 1)
            self.assertEqual(result['failure_code'], 'response_model_mismatch')
            self.assertIsNone(result['response_model'])
            self.assertIsNone(result['selection'])
            self.opener.return_value.open.assert_called_once()

    def test_every_non_stop_finish_reason_fails(self):
        for finish in ('length', 'tool_calls', 'function_call', 'content_filter', None, SECRET):
            self.independent_case()
            self.envelope['choices'][0]['finish_reason'] = finish
            code, result = self.call()
            self.assertEqual(code, 1)
            self.assertFalse(result['citation_valid'])
            self.assertIsNone(result['finding'])
            self.assertIn(result['failure_code'], ('response_truncated', 'response_not_complete'))
            self.opener.return_value.open.assert_called_once()

    def test_missing_content_and_model_refusal_fail_safely(self):
        for content in (None, '', '   ', {}, []):
            self.independent_case()
            self.envelope['choices'][0]['message']['content'] = content
            code, result = self.call()
            self.assertEqual(code, 1)
            self.assertEqual(result['failure_code'], 'missing_content')
            self.opener.return_value.open.assert_called_once()
        self.independent_case()
        self.envelope['choices'][0]['message']['refusal'] = SECRET
        _, result = self.call()
        self.assertEqual(result['failure_code'], 'model_refusal')

    def test_malformed_json_duplicates_nan_unsupported_check_and_citations_fail(self):
        cases = [('bad JSON', 'invalid_selection_json'),
                 ('{"line":39,"line":38}', 'invalid_selection_json'),
                 ('{"line":NaN}', 'invalid_selection_json'),
                 (json.dumps(dict(SELECTION, check='land')), 'unsupported_check'),
                 (json.dumps(dict(SELECTION, line=38)), 'citation_mismatch'),
                 (json.dumps(dict(SELECTION, evidence_id=SECRET)), 'citation_mismatch'),
                 (json.dumps(dict(SELECTION, line=37, evidence_id='0dd069876fac')), 'citation_mismatch'),
                 (json.dumps({'check': 'approval_gate'}), 'missing_citation')]
        for content, expected in cases:
            with self.subTest(expected=expected):
                self.independent_case()
                self.envelope['choices'][0]['message']['content'] = content
                code, result = self.call()
                self.assertEqual(code, 1)
                self.assertEqual(result['failure_code'], expected)
                self.assertIsNone(result['selection'])
                self.assertIsNone(result['finding'])
                self.assertFalse(result['citation_valid'])
                self.opener.return_value.open.assert_called_once()

    def test_missing_credentials_and_mismatched_environment_never_claim_guard(self):
        for env in ({}, {'NEBIUS_API_KEY': SECRET, 'NEBIUS_BASE_URL': 'https://private.example/' + SECRET},
                    {'NEBIUS_API_KEY': SECRET, 'NEBIUS_MODEL': SECRET}):
            with patch.dict('os.environ', env, clear=True):
                code, result = self.call()
            self.assertEqual(code, 1)
            self.assertFalse(self.guard.exists())
        self.opener.assert_not_called()

    def test_only_fixed_trace_window_and_payload_can_be_used(self):
        for window in ((1, 2), (38, 70), (38, 38)):
            args = self.args()
            i = args.index('--line-window')
            args[i+1:i+3] = [str(x) for x in window]
            code, _ = self.call(args)
            self.assertEqual(code, 1)
        args = self.args()
        args[0] = str(n.ROOT / 'evaluation/traces/approval_conflict.jsonl')
        self.assertEqual(self.call(args)[0], 1)
        with patch('nebius_review.ATTEMPT004_PAYLOAD_SHA256', 'changed'):
            self.assertEqual(self.call()[0], 1)
        with patch('nebius_review.ATTEMPT004_TRACE_SHA256', 'changed'):
            self.assertEqual(self.call()[0], 1)
        self.opener.assert_not_called()
        self.assertFalse(self.guard.exists())

    def test_existing_and_protected_output_paths_are_never_overwritten(self):
        out = self.root / 'existing'
        out.mkdir()
        keep = out / 'receipt.json'
        keep.write_text('preserve me')
        self.assertEqual(self.call(self.args(out))[0], 1)
        self.assertEqual(keep.read_text(), 'preserve me')
        for out in (n.ROOT/'evaluation/new', n.ROOT/'approval/new', n.ROOT/'demo/new', n.ROOT/'.git/new'):
            self.assertEqual(self.call(self.args(out))[0], 1)
            self.assertFalse(out.exists())
        self.opener.assert_not_called()
        self.assertFalse(self.guard.exists())

    def test_request_id_falls_back_to_hashed_json_id(self):
        self.response.headers = {}
        _, result = self.call()
        self.assertEqual(result['provider_request_id_sha256'], hashlib.sha256(REQUEST_ID.encode()).hexdigest())

    def test_arbitrary_provider_exception_is_sanitized_and_not_retried(self):
        self.opener.return_value.open.side_effect = RuntimeError(SECRET + str(self.root))
        code, result = self.call()
        self.assertEqual(code, 1)
        self.assertEqual(result['failure_code'], 'provider_unavailable')
        self.opener.return_value.open.assert_called_once()

    def test_no_redirect_or_automatic_parameter_fallback(self):
        self.opener.return_value.open.side_effect = n.ReviewError('Provider redirect refused')
        code, result = self.call()
        self.assertEqual(code, 1)
        self.assertFalse(result['citation_valid'])
        self.assertTrue(self.guard.exists())
        self.opener.return_value.open.assert_called_once()

    def test_frozen_attempt_parameters_match_offline_serialization(self):
        _, _, _, digest, size = n.prepare_attempt004(n.ATTEMPT004_TRACE, n.ATTEMPT004_WINDOW)
        self.assertEqual(digest, n.ATTEMPT004_PAYLOAD_SHA256)
        self.assertEqual(size, 1327)
        self.assertEqual(n.ATTEMPT004_TRACE_SHA256,
                         '82c40c6f132c9191ea5e8d0a03004b73d7a4092311714b902796827ec91d8a98')
        self.assertEqual(n.ATTEMPT004_WINDOW, (38, 39))
        self.assertEqual(n.TOKEN_FACTORY_BASE_URL + '/chat/completions',
                         'https://api.tokenfactory.nebius.com/v1/chat/completions')
        self.assertEqual(n.MAX_OUTPUT_TOKENS, 256)
        self.assertEqual(n.TIMEOUT_SECONDS, 15)
        self.assertEqual(n.MAX_ATTEMPTS, 1)
        self.opener.assert_not_called()

    def test_failed_guard_durability_never_reaches_transport(self):
        args = self.args()
        # First fsync failure consumes conservatively; later receipt fsync works.
        with patch('nebius_review.os.fsync', side_effect=[OSError(SECRET), None]):
            code, result = self.call(args)
        self.assertEqual(code, 1)
        self.assertFalse(result['request_attempted'])
        self.assertTrue(self.guard.exists())
        self.opener.assert_not_called()
        before = self.guard.read_bytes()
        self.call()
        self.assertEqual(self.guard.read_bytes(), before)
        self.opener.assert_not_called()

    def test_invalid_or_oversized_http_envelope_never_retries(self):
        for raw in (b'[]', b'{broken', b'{"model":"x","model":"y"}', b'x' * 262145):
            self.independent_case()
            self.response.read.side_effect = None
            self.response.read.return_value = raw
            code, result = self.call()
            self.assertEqual(code, 1)
            self.assertFalse(result['citation_valid'])
            self.assertTrue(self.guard.exists())
            self.opener.return_value.open.assert_called_once()
