"""Run unittest discovery and offline evaluation; retain allowlisted JSON evidence."""
import io
import argparse
from contextlib import redirect_stdout, redirect_stderr
import hashlib
import json
from pathlib import Path
import platform
import socket
import unittest
from unittest.mock import patch

from model_evaluation import evaluate


def offline_connection(address, *args, **kwargs):
    """Permit the local video test, never an external provider connection."""
    if address[0] != "127.0.0.1":
        raise RuntimeError("External network disabled during local checks")
    return _create_connection(address, *args, **kwargs)


_create_connection = socket.create_connection


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("runs/offline-checks"),
                        help="Fresh results directory; historical evidence is never overwritten")
    args = parser.parse_args(argv)
    output = args.output_dir.resolve()
    protected = Path(__file__).resolve().parent / "evaluation"
    if output.is_relative_to(protected):
        parser.error("Output must be outside historical evaluation evidence")
    if output.exists():
        parser.error("Output already exists; choose a fresh directory")
    output.mkdir(parents=True)
    suite = unittest.defaultTestLoader.discover("tests")
    # Tracebacks/captured provider bodies are not written into the result artifact.
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()), patch(
            "socket.create_connection", side_effect=offline_connection):
        result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=2).run(suite)
    report = {"format_version": 1, "live_api_calls": 0,
              "tests_run": result.testsRun, "successful": result.wasSuccessful(),
              "failures": [test.id() for test, _ in result.failures],
              "errors": [test.id() for test, _ in result.errors],
              "skipped": [test.id() for test, _ in result.skipped]}
    report["python_version"] = platform.python_version()
    report["source_sha256"] = {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
                               for path in sorted(Path(".").rglob("*.py"))
                               if ".git" not in path.parts}
    (output / "local_tests.json").write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    (output / "offline_evaluation.json").write_text(json.dumps(evaluate(), sort_keys=True, indent=2) + "\n")
    print(json.dumps(report, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
