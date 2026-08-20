"""Pick today's task from queue.md.

Selection rule:
    day-of-week -> which weekday section
    ISO-week number % (number of tasks in that section) -> which task

This gives a stable, deterministic rotation per weekday: task 1 in
week 1, task 2 in week 2, wrapping back to task 1 once you've been
through all six. Called by the daily-issue workflow and can be run
locally: `python scripts/pick_task.py`.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

# Windows consoles default to cp1252 and blow up on em-dashes and arrows.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WEEKDAYS = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
}


def parse_queue(queue_path: Path) -> dict[str, list[str]]:
    """Return {weekday_name: [task_line, ...]} parsed from queue.md."""
    sections: dict[str, list[str]] = {name: [] for name in WEEKDAYS.values()}
    current: str | None = None
    task_re = re.compile(r"^\s*\d+\.\s+(.*\S)\s*$")
    for line in queue_path.read_text(encoding="utf-8").splitlines():
        header = re.match(r"^##\s+(\w+)\b", line)
        if header:
            name = header.group(1)
            current = name if name in sections else None
            continue
        if current is None:
            continue
        match = task_re.match(line)
        if match and not match.group(1).lstrip().startswith("~~"):
            sections[current].append(match.group(1))
    return sections


def pick(today: dt.date, sections: dict[str, list[str]]) -> tuple[str, str] | None:
    weekday_name = WEEKDAYS.get(today.weekday())
    if weekday_name is None:
        return None
    tasks = sections.get(weekday_name) or []
    if not tasks:
        return weekday_name, "(no active tasks left for this weekday — add more to queue.md)"
    week_number = today.isocalendar().week
    return weekday_name, tasks[(week_number - 1) % len(tasks)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--date",
        help="ISO date (YYYY-MM-DD). Defaults to today (UTC).",
    )
    parser.add_argument(
        "--queue",
        default="queue.md",
        help="Path to the queue file (default: queue.md).",
    )
    parser.add_argument(
        "--format",
        choices=("plain", "issue"),
        default="plain",
        help="plain = one-line; issue = title + body for the daily-issue workflow.",
    )
    args = parser.parse_args()

    today = dt.date.fromisoformat(args.date) if args.date else dt.datetime.now(dt.UTC).date()
    sections = parse_queue(Path(args.queue))
    picked = pick(today, sections)
    if picked is None:
        print(f"::notice::No rotation for {today.isoformat()} (weekend).", file=sys.stderr)
        return 0

    weekday, task = picked
    if args.format == "issue":
        title = f"[{today.isoformat()}] {weekday} — {task[:90]}"
        body = (
            f"**Date:** {today.isoformat()} ({weekday})\n\n"
            f"**Task:** {task}\n\n"
            "Close this issue when the work is committed to the target repo. "
            "If the task no longer makes sense, edit `queue.md` and note the swap in the close comment."
        )
        print(f"title<<EOF\n{title}\nEOF\nbody<<EOF\n{body}\nEOF")
    else:
        print(f"{weekday}: {task}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
