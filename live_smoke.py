"""One explicitly gated Nebius request on a fixed synthetic trace. Disabled by default."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

from nebius_review import (BASE_URL, MODEL, MAX_OUTPUT_TOKENS, TIMEOUT_SECONDS,
                           MAX_ATTEMPTS, MockProvider, NebiusProvider, ReviewError, review)
from nebius_review import safe_failure_code
from trace_reader import read_trace

TRACE = Path(__file__).resolve().parent / "evaluation/traces/approval_conflict.jsonl"
ATTEMPT_RECORD = Path(__file__).resolve().parent / "evaluation/results/live_attempt_consumed.json"


def claim_attempt(attempt_record=None):
    """Exclusive durable claim prevents command reruns/concurrent attempts. Never auto-reset."""
    try:
        record = ATTEMPT_RECORD if attempt_record is None else attempt_record
        record.parent.mkdir(parents=True, exist_ok=True)
        with record.open("x") as stream:
            json.dump({"allowance_consumed": True, "automatic_retry_allowed": False}, stream)
    except OSError:
        raise ReviewError("Request allowance unavailable; owner review required") from None


def preflight(*, attempt_record=None, base_url=None, max_output_tokens=MAX_OUTPUT_TOKENS):
    """Check local prerequisites without opening a connection or revealing secrets."""
    trace = read_trace(TRACE)
    trace_valid = trace["valid"] and trace["input"]["hash_complete"]
    class Capture(MockProvider):
        def complete(self, messages):
            self.characters = sum(len(m["content"]) for m in messages)
            return super().complete(messages)
    capture = Capture()
    try:
        review(TRACE, capture)
        input_characters = capture.characters
    except ReviewError:
        input_characters = None
    checks = {"fixed_trace_valid": trace_valid,
              "input_approximately_under_1000_tokens": input_characters is not None and input_characters <= 2000,
              "output_limit_valid": type(max_output_tokens) is int and max_output_tokens in (256, 1024),
              "short_timeout": 0 < TIMEOUT_SECONDS <= 15,
              "one_attempt_limit": MAX_ATTEMPTS == 1,
              "attempt_allowance_unused": not (ATTEMPT_RECORD if attempt_record is None else attempt_record).exists()}
    try:
        if base_url is None and max_output_tokens == MAX_OUTPUT_TOKENS:
            NebiusProvider.from_env()
        else:
            NebiusProvider.from_env(expected_base_url=base_url, max_output_tokens=max_output_tokens)
        configuration_valid = True
    except ReviewError:
        configuration_valid = False
    return {"format_version": 1, "mode": "offline_preflight",
            "request_attempted": False, "live_api_calls": 0,
            "trace_valid": trace_valid, "input_sha256": trace["input"]["sha256"],
            "credential_and_configuration_valid": configuration_valid,
            "code_checks": checks, "code_conditions_pass": all(checks.values()),
            "input_characters": input_characters, "input_tokens_are_estimated": True,
            "max_output_tokens": max_output_tokens, "timeout_seconds": TIMEOUT_SECONDS,
            "billing_cap_verified": False, "live_ready": False,
            "owner_authorization": "required_before_live_request",
            "account_access_quota_pricing": "not_verified",
            "ready_for_authorized_attempt": bool(all(checks.values()) and configuration_valid)}


def main(argv=None, *, attempt_record=None, attempt_id=None, base_url=None, evidence_path=None,
         max_output_tokens=MAX_OUTPUT_TOKENS):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-paid-api", action="store_true")
    parser.add_argument("--owner-authorization", choices=("one-synthetic-request",))
    billing = parser.add_mutually_exclusive_group()
    billing.add_argument("--account-cap-confirmed", action="store_true",
                        help="Owner attests an enforceable account-side cap <= $1, not an alert or estimate")
    billing.add_argument("--owner-accepts-no-account-cap", action="store_true",
                         help="Owner explicitly accepts no account-side cap for this one request")
    parser.add_argument("--preflight", action="store_true",
                        help="Check local prerequisites offline; never issue a request")
    args = parser.parse_args(argv)
    if args.preflight:
        report = preflight(attempt_record=attempt_record, base_url=base_url, max_output_tokens=max_output_tokens)
        if attempt_id is not None:
            report["attempt_id"] = attempt_id
        print(json.dumps(report, sort_keys=True))
        return 0 if report["ready_for_authorized_attempt"] else 1
    # Neither a key nor ordinary test discovery enables network activity.
    if not args.allow_paid_api or args.owner_authorization != "one-synthetic-request":
        print(json.dumps({"status": "disabled", "request_attempted": False,
                          "reason": "explicit_owner_authorization_required"}))
        return 2
    if not (args.account_cap_confirmed or args.owner_accepts_no_account_cap):
        print(json.dumps({"status": "disabled", "request_attempted": False,
                          "reason": "explicit_billing_authorization_required"}))
        return 2
    attempted = False
    evidence_stream = None
    report = {"format_version": 1, "provider": "nebius", "model": MODEL,
              "billing_authorization": ("owner_accepts_no_account_cap"
                                        if args.owner_accepts_no_account_cap else "account_cap_confirmed"),
              "endpoint": (base_url or BASE_URL) + "/chat/completions", "synthetic": True,
              "max_output_tokens": max_output_tokens,
              "timestamp_utc": datetime.now(timezone.utc).isoformat(), "hardware_action": False}
    provider = None
    if attempt_id is not None:
        report["attempt_id"] = attempt_id
    try:
        provider = (NebiusProvider.from_env() if base_url is None and max_output_tokens == MAX_OUTPUT_TOKENS
                    else NebiusProvider.from_env(expected_base_url=base_url, max_output_tokens=max_output_tokens))
        if evidence_path is not None:
            try:
                evidence_path.parent.mkdir(parents=True, exist_ok=True)
                evidence_stream = evidence_path.open("x")
            except OSError:
                raise ReviewError("Evidence destination unavailable; existing evidence preserved") from None
        # review validates the fixed trace before invoking this wrapper.
        class CountedProvider:
            def complete(self, messages):
                nonlocal attempted
                if attempted:
                    raise ReviewError("Single request allowance already consumed")
                if sum(len(m["content"]) for m in messages) > 2000:
                    raise ReviewError("Smoke input exceeds local size limit")
                claim_attempt(attempt_record)
                attempted = True
                return provider.complete(messages)
        result = review(TRACE, CountedProvider())
        if provider.metadata.get("response_model") != MODEL:
            raise ReviewError("Returned model identity missing or mismatched", "response_model_mismatch")
        # Strict allowlist: never print content, headers, IDs or error text from the API.
        report.update(status="verified", input_sha256=result["input_sha256"],
                      citation_valid=True, check_valid=True, usage=provider.usage,
                      matches_synthetic_expectation=(result["selection"] == {
                          "line": 2, "evidence_id": "synthetic-approval_conflict-1", "check": "approval_gate"}
                          and result["finding"] == "reported_execution_without_recorded_approval"))
        code = 0
    except ReviewError as error:
        report.update(status="not_verified", reason="configuration_provider_or_validation_failure",
                      failure_code=safe_failure_code(error))
        code = 1
    if provider is not None:
        report.update(provider.metadata)
        report["usage"] = provider.usage
        report["cost_basis"] = "usage counts at published $0.30/M input and $0.90/M output; not a spending cap"
    report["request_attempted"] = attempted
    if evidence_stream is not None:
        with evidence_stream:
            evidence_stream.write(json.dumps(report, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
