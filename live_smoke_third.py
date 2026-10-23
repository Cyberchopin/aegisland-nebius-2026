"""Attempt 003 candidate only. Requires separate final owner execution authorization."""
from pathlib import Path

import live_smoke
from nebius_review import TOKEN_FACTORY_BASE_URL

ATTEMPT_ID = "b3-smoke-003"
MAX_OUTPUT_TOKENS = 1024
RESULTS = Path(__file__).resolve().parent / "evaluation/results"
ATTEMPT_RECORD = RESULTS / "live_attempt_003_consumed.json"
EVIDENCE_PATH = RESULTS / "live_smoke_003.json"


def main(argv=None):
    return live_smoke.main(argv, attempt_record=ATTEMPT_RECORD,
                           attempt_id=ATTEMPT_ID, base_url=TOKEN_FACTORY_BASE_URL,
                           evidence_path=EVIDENCE_PATH, max_output_tokens=MAX_OUTPUT_TOKENS)


if __name__ == "__main__":
    raise SystemExit(main())
