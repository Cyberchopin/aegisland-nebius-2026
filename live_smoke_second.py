"""Second independent smoke attempt. Execution requires separate owner final GO."""
from pathlib import Path

import live_smoke
from nebius_review import TOKEN_FACTORY_BASE_URL

ATTEMPT_ID = "b2-smoke-002"
RESULTS = Path(__file__).resolve().parent / "evaluation/results"
ATTEMPT_RECORD = RESULTS / "live_attempt_002_consumed.json"
EVIDENCE_PATH = RESULTS / "live_smoke_002.json"


def main(argv=None):
    return live_smoke.main(argv, attempt_record=ATTEMPT_RECORD,
                           attempt_id=ATTEMPT_ID, base_url=TOKEN_FACTORY_BASE_URL,
                           evidence_path=EVIDENCE_PATH)


if __name__ == "__main__":
    raise SystemExit(main())
