# daily-log

A public record of my daily engineering rotation. One real, small
piece of work per weekday across my pinned repos and a Today-I-Learned
stream — no streak-keepers, no auto-commits, no green-square farming.

Every task in [`queue.md`](queue.md) is a specific unit of work drawn
from a real gap I know exists in one of my repos. A GitHub Action
opens an issue on this repo every weekday at 9:00 AM Central Time
with the day's task; I close the issue when the work lands (usually
in another repo). On Sundays, a second workflow appends a weekly
review to `reviews/`.

## Rotation

| Day | Kind of work                                                      |
| --- | ----------------------------------------------------------------- |
| Mon | New eval case in [`agent-evals`](https://github.com/Sonteru4/agent-evals) |
| Tue | TIL note — a real thing learned that day, min 150 words           |
| Wed | Documentation improvement on a pinned repo                        |
| Thu | Refactor or bugfix on a pinned repo, with the test that motivates it |
| Fri | Dependency update or CI improvement                               |

Weekends are unscheduled.

## Layout

```
queue.md              # ordered backlog — one task per weekday
scripts/
  pick_task.py        # prints today's task based on weekday + queue
  weekly_review.py    # scans last 7 days of my public commits
.github/workflows/
  daily-issue.yml     # opens the daily task issue
  weekly-review.yml   # runs pick_task on Sundays and appends to reviews/
reviews/              # weekly digest of what actually landed
```

## Why this exists, honestly

I noticed my contribution graph looked like a batch push rather than
lived-in activity, and no amount of cosmetic fixing solves that —
only weeks of small, real commits do. This repo is the scaffolding.
