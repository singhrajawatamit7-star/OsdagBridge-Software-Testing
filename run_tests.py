"""Run the QA test suite using the real Pytest runner."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-v",
        "--tb=short",
        str(ROOT / "tests"),
    ]
    result = subprocess.run(command, cwd=ROOT)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
