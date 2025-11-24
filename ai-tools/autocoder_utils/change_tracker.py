from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Sequence


def _argv_or_sys(argv: Sequence[str] | None) -> Sequence[str]:
    return argv if argv is not None else sys.argv


def find_most_recent_change_file(changes_dir: Path) -> datetime | None:
    """
    Find the most recent change file by parsing filenames in year/month subdirectories.
    """
    if not changes_dir.exists():
        changes_dir.mkdir(parents=True, exist_ok=True)
        return None

    pattern = re.compile(r"^(\d{4}-\d{2}-\d{2})-CHANGES\.md$")

    dates = []
    for file in changes_dir.rglob("*-CHANGES.md"):
        if file.is_file():
            match = pattern.match(file.name)
            if match:
                try:
                    date = datetime.strptime(match.group(1), "%Y-%m-%d")
                    dates.append(date)
                except ValueError:
                    continue

    return max(dates) if dates else None


def get_git_changes(since_date: datetime | None) -> list[dict] | None:
    """
    Get git changes since the specified date.
    """
    cmd = [
        "git",
        "log",
        "--pretty=format:%H|%ai|%an|%s",
    ]

    if since_date:
        since_str = (since_date + timedelta(days=1)).strftime("%Y-%m-%d")
        cmd.append(f"--since={since_str}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"Error running git log: {exc}", file=sys.stderr)
        return None

    commits = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue

        parts = line.split("|", 3)
        if len(parts) == 4:
            commits.append(
                {
                    "hash": parts[0][:8],
                    "date": parts[1].split()[0],
                    "author": parts[2],
                    "message": parts[3],
                }
            )

    return commits


def get_git_stats(since_date: datetime | None) -> dict | None:
    """
    Aggregate file statistics since the specified date by summing per-commit stats.
    """
    cmd = ["git", "log", "--numstat", "--format=%H"]
    if since_date:
        since_str = (since_date + timedelta(days=1)).strftime("%Y-%m-%d")
        cmd.extend(["--since", since_str])
    cmd.append("HEAD")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"Error running git log for stats: {exc}", file=sys.stderr)
        return None

    files_touched: set[str] = set()
    insertions_total = 0
    deletions_total = 0

    for line in result.stdout.splitlines():
        if "\t" not in line:
            continue
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        insertions_raw, deletions_raw, path = parts
        if not path:
            continue

        try:
            insertions = int(insertions_raw)
        except ValueError:
            insertions = 0
        try:
            deletions = int(deletions_raw)
        except ValueError:
            deletions = 0

        files_touched.add(path)
        insertions_total += insertions
        deletions_total += deletions

    return {
        "files_changed": len(files_touched),
        "insertions": insertions_total,
        "deletions": deletions_total,
    }


def get_closed_issues(since_date: datetime | None) -> list[dict] | None:
    """
    Get closed GitHub issues since the specified date.
    """
    cmd = [
        "gh",
        "issue",
        "list",
        "--state",
        "closed",
        "--json",
        "number,title,closedAt,url",
        "--limit",
        "1000",
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"Error running gh issue list: {exc}", file=sys.stderr)
        print("Make sure 'gh' CLI is installed and authenticated", file=sys.stderr)
        return None

    try:
        all_issues = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"Error parsing issue JSON: {exc}", file=sys.stderr)
        return None

    if since_date:
        since_str = (since_date + timedelta(days=1)).strftime("%Y-%m-%d")
        filtered_issues = []
        for issue in all_issues:
            if issue["closedAt"]:
                closed_date = issue["closedAt"].split("T")[0]
                if closed_date >= since_str:
                    filtered_issues.append(
                        {
                            "number": issue["number"],
                            "title": issue["title"],
                            "closed_at": closed_date,
                            "url": issue["url"],
                        }
                    )
        return filtered_issues

    return [
        {
            "number": issue["number"],
            "title": issue["title"],
            "closed_at": issue["closedAt"].split("T")[0] if issue["closedAt"] else "unknown",
            "url": issue["url"],
        }
        for issue in all_issues
    ]


def get_closed_prs(since_date: datetime | None) -> list[dict] | None:
    """
    Get merged GitHub pull requests since the specified date.
    """
    cmd = [
        "gh",
        "pr",
        "list",
        "--state",
        "merged",
        "--json",
        "number,title,mergedAt,url",
        "--limit",
        "100",
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"Error running gh pr list: {exc}", file=sys.stderr)
        stderr_output = exc.stderr if hasattr(exc, "stderr") else "No stderr available"
        print(f"Error details: {stderr_output}", file=sys.stderr)
        print("Make sure 'gh' CLI is installed and authenticated", file=sys.stderr)
        return None

    try:
        all_prs = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"Error parsing PR JSON: {exc}", file=sys.stderr)
        return None

    if since_date:
        since_str = (since_date + timedelta(days=1)).strftime("%Y-%m-%d")
        filtered_prs = []
        for pr in all_prs:
            if pr["mergedAt"]:
                merged_date = pr["mergedAt"].split("T")[0]
                if merged_date >= since_str:
                    filtered_prs.append(
                        {
                            "number": pr["number"],
                            "title": pr["title"],
                            "merged_at": merged_date,
                            "url": pr["url"],
                        }
                    )
        return filtered_prs

    return [
        {
            "number": pr["number"],
            "title": pr["title"],
            "merged_at": pr["mergedAt"].split("T")[0] if pr["mergedAt"] else "unknown",
            "url": pr["url"],
        }
        for pr in all_prs
    ]


def format_changes_markdown(
    commits: list[dict],
    stats: dict,
    since_date: datetime | None,
    issues: list[dict] | None = None,
    prs: list[dict] | None = None,
) -> str:
    """
    Format git changes as markdown, grouping issues with their closing PRs.
    """
    if issues is None:
        issues = []
    if prs is None:
        prs = []

    today = datetime.now().strftime("%Y-%m-%d")

    lines = [
        f"# Changes for {today}",
        "",
    ]

    if since_date:
        lines.append(f"Changes since {since_date.strftime('%Y-%m-%d')}")
    else:
        lines.append("All changes")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Commits**: {len(commits)}")
    lines.append(f"- **Pull Requests**: {len(prs)}")
    lines.append(f"- **Issues Closed**: {len(issues)}")
    lines.append(f"- **Files Changed**: {stats['files_changed']}")
    lines.append(f"- **Insertions**: +{stats['insertions']}")
    lines.append(f"- **Deletions**: -{stats['deletions']}")
    lines.append("")

    issue_to_pr = {}
    for pr in prs:
        issue_match = re.search(r"#(\d+)", pr["title"])
        if issue_match:
            issue_number = int(issue_match.group(1))
            matching_issue = next((issue for issue in issues if issue["number"] == issue_number), None)
            if matching_issue:
                issue_to_pr[issue_number] = pr

    if issues:
        lines.append("## Issues")
        lines.append("")
        for issue in sorted(issues, key=lambda x: x["closed_at"], reverse=True):
            lines.append(f"### Issue #{issue['number']}: {issue['title']}")
            lines.append(f"Closed: {issue['closed_at']}")
            lines.append(f"URL: {issue['url']}")
            lines.append("")

            closing_pr = issue_to_pr.get(issue["number"])
            if closing_pr:
                lines.append("**Closed by:**")
                lines.append(f"- PR #{closing_pr['number']}: {closing_pr['title']}")
                lines.append(f"  - Merged: {closing_pr['merged_at']}")
                lines.append(f"  - URL: {closing_pr['url']}")
                lines.append("")

    pr_numbers_with_issues = {pr["number"] for pr in issue_to_pr.values()}
    standalone_prs = [pr for pr in prs if pr["number"] not in pr_numbers_with_issues]

    if standalone_prs:
        lines.append("## Pull Requests")
        lines.append("")
        for pr in sorted(standalone_prs, key=lambda x: x["merged_at"], reverse=True):
            lines.append(f"### PR #{pr['number']}: {pr['title']}")
            lines.append(f"Merged: {pr['merged_at']}")
            lines.append(f"URL: {pr['url']}")
            lines.append("")

    commit_to_pr = {}
    for commit in commits:
        pr_match = re.search(r"#(\d+)", commit["message"])
        if pr_match:
            pr_number = int(pr_match.group(1))
            matching_pr = next((pr for pr in prs if pr["number"] == pr_number), None)
            if matching_pr:
                commit_to_pr[commit["hash"]] = matching_pr

    standalone_commits = [c for c in commits if c["hash"] not in commit_to_pr]
    if standalone_commits:
        lines.append("## Git Commits")
        lines.append("")
        for commit in sorted(standalone_commits, key=lambda x: x["date"], reverse=True):
            lines.append(f"- `{commit['hash']}` {commit['message']}")
            lines.append(f"  - Author: {commit['author']}")
            lines.append(f"  - Date: {commit['date']}")
        lines.append("")

    return "\n".join(lines)


def generate_changelog(argv: Sequence[str] | None = None) -> None:
    """
    Main entry point for the change tracker.
    """
    _argv_or_sys(argv)  # allows optional argv for parity with other commands
    repo_root = Path.cwd()
    changes_dir = repo_root / "changes"

    required = ["git", "gh"]
    missing = [cmd for cmd in required if not shutil.which(cmd)]
    if missing:
        print(f"Error: Missing required commands: {', '.join(missing)}", file=sys.stderr)
        raise SystemExit(1)

    print("Change Tracker")
    print("=" * 50)

    most_recent_date = find_most_recent_change_file(changes_dir)
    if most_recent_date:
        print(f"Most recent change file: {most_recent_date.strftime('%Y-%m-%d')}")
    else:
        print("No previous change files found - tracking all changes")

    print("Fetching git changes...")
    commits = get_git_changes(most_recent_date)
    if commits is None:
        print("Failed to fetch git changes. Aborting.", file=sys.stderr)
        raise SystemExit(1)

    stats = get_git_stats(most_recent_date)
    if stats is None:
        print("Failed to fetch git stats. Aborting.", file=sys.stderr)
        raise SystemExit(1)

    print(f"Found {len(commits)} commits")

    print("Fetching closed GitHub issues...")
    issues = get_closed_issues(most_recent_date)
    if issues is None:
        print("Failed to fetch closed issues from GitHub. Aborting.", file=sys.stderr)
        raise SystemExit(1)
    print(f"Found {len(issues)} closed issues")

    print("Fetching merged GitHub pull requests...")
    prs = get_closed_prs(most_recent_date)
    if prs is None:
        print("Failed to fetch merged pull requests from GitHub. Aborting.", file=sys.stderr)
        raise SystemExit(1)
    print(f"Found {len(prs)} merged PRs")

    no_recent_activity = (
        most_recent_date is not None
        and not commits
        and not issues
        and not prs
        and stats.get("files_changed", 0) == 0
    )

    if no_recent_activity:
        print("No new changes since the last changelog. Skipping file generation.")
        return

    markdown = format_changes_markdown(commits, stats, most_recent_date, issues, prs)

    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%B")
    today = now.strftime("%Y-%m-%d")

    output_dir = changes_dir / year / month
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{today}-CHANGES.md"
    output_file.write_text(markdown)

    print(f"Changes written to: {output_file}")
    print("=" * 50)
