
from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence

from .address_pr_comments import (
    address_pr_comments_with_codex as _address_pr_comments_with_codex,
    address_pr_comments_with_claude as _address_pr_comments_with_claude,
    address_pr_comments_with_kilocode as _address_pr_comments_with_kilocode,
)
from .change_tracker import generate_changelog as _generate_changelog
from .gh_pr_helper import gh_pr_helper as _gh_pr_helper
from .issue_workflow import IssueWorkflowConfig, run_issue_workflow


def _argv(argv: Sequence[str] | None) -> Sequence[str]:
    return argv if argv is not None else sys.argv


def _parse_timeout_arg(
    argv: Sequence[str] | None, default: int
) -> tuple[Sequence[str], int]:
    """Return argv without the timeout option and the parsed timeout value."""
    args = list(_argv(argv))
    parsed_args: list[str] = []
    timeout = default
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith("--timeout="):
            _, value = arg.split("=", 1)
            timeout = _parse_timeout_value(value)
        elif arg == "--timeout":
            if i + 1 >= len(args):
                raise SystemExit("Missing value for --timeout")
            i += 1
            timeout = _parse_timeout_value(args[i])
        else:
            parsed_args.append(arg)
        i += 1
    return parsed_args, timeout


def _parse_timeout_value(value: str) -> int:
    """Parse a timeout value ensuring it is a positive integer."""
    try:
        timeout = int(value)
    except ValueError:
        raise SystemExit(f"Invalid timeout value: {value!r}")
    if timeout <= 0:
        raise SystemExit(f"Timeout must be greater than zero (got {timeout})")
    return timeout



def fix_issue_with_kilocode(argv: Sequence[str] | None = None) -> None:
    """CLI wrapper for the kilocode issue workflow."""
    args, timeout = _parse_timeout_arg(argv, default=1200)
    config = IssueWorkflowConfig(
        tool_cmd=["kilocode", "--auto"],
        branch_prefix="fix-kilocode",
        default_commit_message="Update from kilocode",
        timeout_seconds=timeout,
    )
    run_issue_workflow(args, config)


def fix_issue_with_claude(argv: Sequence[str] | None = None) -> None:
    """CLI wrapper for the claude issue workflow with headless mode."""
    # Determine session directory (prefer ./paige relative to cwd)
    session_dir = Path.cwd() / "paige"

    args, timeout = _parse_timeout_arg(argv, default=180)
    config = IssueWorkflowConfig(
        tool_cmd=[
            "claude",
            "-p",
            "fix this issue",
            "--permission-mode",
            "acceptEdits",
        ],
        branch_prefix="fix-claude",
        default_commit_message="Update from claude",
        timeout_seconds=timeout,
        session_dir=session_dir,
        use_json_output=True,
    )
    run_issue_workflow(args, config)


def fix_issue_with_codex(argv: Sequence[str] | None = None) -> None:
    """CLI wrapper for the Codex issue workflow."""
    args, timeout = _parse_timeout_arg(argv, default=180)
    config = IssueWorkflowConfig(
        tool_cmd=[
            "codex",
            "exec",
            "--full-auto",
            "--sandbox",
            "danger-full-access",
            "-",
        ],
        branch_prefix="fix-codex",
        default_commit_message="Update from codex",
        timeout_seconds=timeout,
        input_instruction=(
            "You are Codex running headless. Fix the GitHub issue described below using this "
            "repository. Apply edits, run relevant tests, and finish with a brief summary."
        ),
    )
    run_issue_workflow(args, config)


def address_pr_comments_with_kilocode(argv: Sequence[str] | None = None) -> None:
    """CLI wrapper for addressing PR comments using Kilocode."""
    args, timeout = _parse_timeout_arg(argv, default=1200)
    _address_pr_comments_with_kilocode(args, timeout_seconds=timeout)


def address_pr_comments_with_claude(argv: Sequence[str] | None = None) -> None:
    """CLI wrapper for addressing PR comments using Claude Code."""
    args, timeout = _parse_timeout_arg(argv, default=180)
    _address_pr_comments_with_claude(args, timeout_seconds=timeout)


def address_pr_comments_with_codex(argv: Sequence[str] | None = None) -> None:
    """CLI wrapper for addressing PR comments using Codex."""
    args, timeout = _parse_timeout_arg(argv, default=180)
    _address_pr_comments_with_codex(args, timeout_seconds=timeout)


def generate_changelog(argv: Sequence[str] | None = None) -> None:
    """CLI wrapper for the change tracker."""
    _generate_changelog(_argv(argv))


def gh_pr_helper(argv: Sequence[str] | None = None) -> None:
    """CLI wrapper for the PR helper."""
    _gh_pr_helper(_argv(argv))
