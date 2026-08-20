"""Weekly review: scan public commits from the last 7 days, write a digest.

Uses the GitHub API (`GITHUB_TOKEN` env var, or unauthenticated for a
low rate limit) and hits the events endpoint for the configured user.
Writes `reviews/<iso-year>-W<iso-week>.md` and prints its path.

Run locally: `python scripts/weekly_review.py --user Sonteru4`
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path


def fetch_events(user: str, token: str | None) -> list[dict]:
    events: list[dict] = []
    for page in range(1, 4):  # up to 300 events
        req = urllib.request.Request(
            f"https://api.github.com/users/{user}/events/public?per_page=100&page={page}",
            headers={"Accept": "application/vnd.github+json"},
        )
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                page_events = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            print(f"::warning::events fetch failed: {e}", file=sys.stderr)
            break
        if not page_events:
            break
        events.extend(page_events)
    return events


def summarise(events: list[dict], since: dt.datetime) -> dict:
    commits_by_repo: dict[str, list[str]] = defaultdict(list)
    prs: list[str] = []
    issues_opened: list[str] = []
    issues_closed: list[str] = []
    for ev in events:
        created = dt.datetime.fromisoformat(ev["created_at"].replace("Z", "+00:00"))
        if created < since:
            continue
        repo = ev.get("repo", {}).get("name", "?")
        etype = ev.get("type")
        payload = ev.get("payload", {}) or {}
        if etype == "PushEvent":
            for c in payload.get("commits", []):
                msg = (c.get("message") or "").splitlines()[0]
                commits_by_repo[repo].append(msg)
        elif etype == "PullRequestEvent" and payload.get("action") == "opened":
            pr = payload.get("pull_request", {})
            prs.append(f"{repo}#{pr.get('number')} — {pr.get('title')}")
        elif etype == "IssuesEvent":
            issue = payload.get("issue", {})
            entry = f"{repo}#{issue.get('number')} — {issue.get('title')}"
            if payload.get("action") == "opened":
                issues_opened.append(entry)
            elif payload.get("action") == "closed":
                issues_closed.append(entry)
    return {
        "commits_by_repo": commits_by_repo,
        "prs": prs,
        "issues_opened": issues_opened,
        "issues_closed": issues_closed,
    }


def render(summary: dict, week_start: dt.date, week_end: dt.date) -> str:
    lines = [
        f"# Week of {week_start.isoformat()} – {week_end.isoformat()}",
        "",
    ]

    commits = summary["commits_by_repo"]
    if commits:
        total = sum(len(v) for v in commits.values())
        lines += [f"## Commits ({total} across {len(commits)} repos)", ""]
        for repo, msgs in sorted(commits.items()):
            lines.append(f"### {repo}")
            for m in msgs:
                lines.append(f"- {m}")
            lines.append("")
    else:
        lines += ["## Commits", "", "_None this week._", ""]

    if summary["prs"]:
        lines += ["## Pull requests opened", ""] + [f"- {p}" for p in summary["prs"]] + [""]

    if summary["issues_closed"]:
        lines += ["## Issues closed", ""] + [f"- {i}" for i in summary["issues_closed"]] + [""]

    if summary["issues_opened"]:
        lines += ["## Issues opened", ""] + [f"- {i}" for i in summary["issues_opened"]] + [""]

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", default=os.environ.get("REVIEW_USER", "Sonteru4"))
    parser.add_argument("--out-dir", default="reviews")
    args = parser.parse_args()

    now = dt.datetime.now(dt.UTC)
    since = now - dt.timedelta(days=7)
    events = fetch_events(args.user, os.environ.get("GITHUB_TOKEN"))
    summary = summarise(events, since)

    week = now.isocalendar()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{week.year}-W{week.week:02d}.md"
    out_path.write_text(
        render(summary, since.date(), now.date()),
        encoding="utf-8",
    )
    print(str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
