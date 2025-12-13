#!/usr/bin/env python3
"""Measure xpath library load time and log it to docs/xpath_library_load_times.csv."""

from __future__ import annotations

import subprocess
import time
from pathlib import Path


def _repo_root() -> Path:
    """Return repository root path."""
    return Path(__file__).resolve().parent.parent


def _short_commit_hash(repo_root: Path) -> str:
    """Return the current short git commit hash."""
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _run_xpath_load(repo_root: Path) -> float:
    """Run xpath library load command and return elapsed seconds."""
    command = ["uv", "run", "vibeprolog.py", "./library/xpath.pl", '-q', 'true.']
    start = time.perf_counter()
    subprocess.run(command, cwd=repo_root, check=True)
    return time.perf_counter() - start


def _append_result(repo_root: Path, commit_hash: str, elapsed: float) -> None:
    """Append measurement row to docs/xpath_library_load_times.csv."""
    log_path = repo_root / "docs" / "xpath_library_load_times.csv"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(f"{commit_hash},{elapsed:.2f}\n")


def main() -> None:
    """Run timing measurement and append result."""
    repo_root = _repo_root()
    commit_hash = _short_commit_hash(repo_root)
    elapsed = _run_xpath_load(repo_root)
    _append_result(repo_root, commit_hash, elapsed)
    print(f"Commit {commit_hash} load time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
