"""Executes the routine in order and hands back the report.

Three properties matter more than anything else here:

1. **A failing step does not stop the run.** If the admin panel is down, the
   pankeka post still goes out. Every step is isolated; a failure becomes a
   line in the report and the runner moves on.

2. **A step does not happen twice in a day.** The daily and hourly jobs share
   this machinery, and a crashed run gets retried — neither may republish a
   post. Completed steps are recorded per day and skipped on a second pass.

3. **A dry run leaves no trace.** It records nothing as done, so it cannot
   suppress the real run that follows.
"""

from __future__ import annotations

import json
import traceback
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Callable

from .report import Report, Section


class StepContext:
    """What a step is handed: somewhere to write, and whether this is for real."""

    def __init__(self, report: Report, section: Section, dry_run: bool):
        self.report = report
        self.section = section
        self.dry_run = dry_run

    def feito(self, what: str, detail: str | None = None, link: str | None = None) -> None:
        self.report.feito(self.section, what, detail, link)

    def atencao(self, what: str, detail: str | None = None, link: str | None = None) -> None:
        self.report.atencao(self.section, what, detail, link)


@dataclass
class Step:
    key: str                     # stable id, e.g. "post:anova.autismo" — used for idempotency
    title: str                   # section heading in the report
    run: Callable[[StepContext], None]
    once_per_day: bool = True    # False for the hourly checks


class DayState:
    """Which steps have already run today.

    Keyed by day so the file self-expires: yesterday's entries are ignored
    and overwritten rather than accumulating.
    """

    def __init__(self, path: str | Path, today: date | None = None):
        self.path = Path(path)
        self.today = (today or date.today()).isoformat()
        self._done: set[str] = set()
        self._load()

    def _load(self) -> None:
        try:
            stored = json.loads(self.path.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return
        if stored.get("day") == self.today:
            self._done = set(stored.get("done", []))

    def is_done(self, key: str) -> bool:
        return key in self._done

    def mark(self, key: str) -> None:
        self._done.add(key)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps({"day": self.today, "done": sorted(self._done)}, indent=1))


class Runner:
    def __init__(self, report: Report, state: DayState, *, dry_run: bool = False):
        self.report = report
        self.state = state
        self.dry_run = dry_run
        self.steps: list[Step] = []

    def add(self, step: Step) -> "Runner":
        self.steps.append(step)
        return self

    def run_all(self) -> Report:
        for step in self.steps:
            if step.once_per_day and self.state.is_done(step.key):
                continue  # already handled today; silent, not worth a report line

            section = self.report.section(step.title)
            context = StepContext(self.report, section, self.dry_run)
            try:
                step.run(context)
            except Exception as exc:
                self.report.falhou(section, step.title, _describe(exc))
                continue

            # Only a real, successful run counts. A dry run must not suppress
            # the live one, and a failed step must be retried.
            if step.once_per_day and not self.dry_run:
                self.state.mark(step.key)

        return self.report


def _describe(exc: Exception) -> str:
    """One line for the report, with the call site for the log."""
    where = traceback.extract_tb(exc.__traceback__)[-1] if exc.__traceback__ else None
    location = f" ({where.filename.split('/')[-1]}:{where.lineno})" if where else ""
    return f"{type(exc).__name__}: {exc}{location}"
