"""Tests for the runner — chiefly its three promises: isolation, no repeats,
and that a dry run leaves no trace.

    python -m secretary.test_runner
"""

import json
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path

from .report import Report, Status
from .runner import DayState, Runner, Step


def _step(key, log, *, fails=False, once=True):
    def run(ctx):
        log.append(key)
        if fails:
            raise RuntimeError("painel fora do ar")
        ctx.feito(f"{key} concluído")
    return Step(key=key, title=key, run=run, once_per_day=once)


class RunnerCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.state_path = Path(self.tmp.name) / "state.json"
        self.log = []

    def _runner(self, *, dry_run=False, today=None):
        return Runner(
            Report(datetime(2026, 9, 3, 7, 0)),
            DayState(self.state_path, today=today or date(2026, 9, 3)),
            dry_run=dry_run,
        )


class TestOrderAndIsolation(RunnerCase):
    def test_steps_run_in_order(self):
        r = self._runner()
        for k in ("a", "b", "c"):
            r.add(_step(k, self.log))
        r.run_all()
        self.assertEqual(self.log, ["a", "b", "c"])

    def test_a_failing_step_does_not_stop_the_rest(self):
        r = self._runner()
        r.add(_step("post", self.log))
        r.add(_step("painel", self.log, fails=True))
        r.add(_step("pankeka", self.log))
        r.run_all()
        self.assertEqual(self.log, ["post", "painel", "pankeka"])

    def test_the_failure_reaches_the_report(self):
        r = self._runner()
        r.add(_step("painel", self.log, fails=True))
        rendered = r.run_all().render()
        self.assertIn("painel fora do ar", rendered)
        self.assertIn("PRECISAM DE VOCÊ", rendered)

    def test_failure_names_the_exception_type_and_place(self):
        r = self._runner()
        r.add(_step("painel", self.log, fails=True))
        report = r.run_all()
        detail = [e for e in report._all if e.status is Status.FALHOU][0].detail
        self.assertIn("RuntimeError", detail)
        self.assertIn("test_runner.py:", detail)


class TestIdempotency(RunnerCase):
    def test_a_completed_step_does_not_repeat(self):
        self._runner().add(_step("post", self.log)).run_all()
        self._runner().add(_step("post", self.log)).run_all()
        self.assertEqual(self.log, ["post"])

    def test_a_failed_step_is_retried(self):
        self._runner().add(_step("painel", self.log, fails=True)).run_all()
        self._runner().add(_step("painel", self.log, fails=True)).run_all()
        self.assertEqual(self.log, ["painel", "painel"])

    def test_hourly_steps_repeat_by_design(self):
        for _ in range(3):
            self._runner().add(_step("check", self.log, once=False)).run_all()
        self.assertEqual(self.log, ["check"] * 3)

    def test_a_new_day_starts_clean(self):
        self._runner(today=date(2026, 9, 3)).add(_step("post", self.log)).run_all()
        self._runner(today=date(2026, 9, 4)).add(_step("post", self.log)).run_all()
        self.assertEqual(self.log, ["post", "post"])


class TestDryRun(RunnerCase):
    def test_dry_run_does_not_suppress_the_real_run(self):
        self._runner(dry_run=True).add(_step("post", self.log)).run_all()
        self._runner().add(_step("post", self.log)).run_all()
        self.assertEqual(self.log, ["post", "post"])

    def test_dry_run_writes_no_state_file(self):
        self._runner(dry_run=True).add(_step("post", self.log)).run_all()
        self.assertFalse(self.state_path.exists())

    def test_steps_can_see_they_are_dry(self):
        seen = []
        r = self._runner(dry_run=True)
        r.add(Step("x", "x", lambda ctx: seen.append(ctx.dry_run)))
        r.run_all()
        self.assertEqual(seen, [True])


class TestStateFile(RunnerCase):
    def test_corrupt_state_is_ignored_not_fatal(self):
        self.state_path.write_text("{not json")
        self._runner().add(_step("post", self.log)).run_all()
        self.assertEqual(self.log, ["post"])

    def test_state_records_the_day_and_the_keys(self):
        self._runner().add(_step("post", self.log)).run_all()
        stored = json.loads(self.state_path.read_text())
        self.assertEqual(stored["day"], "2026-09-03")
        self.assertEqual(stored["done"], ["post"])

    def test_missing_directory_is_created(self):
        self.state_path = Path(self.tmp.name) / "deep" / "nested" / "state.json"
        self._runner().add(_step("post", self.log)).run_all()
        self.assertTrue(self.state_path.exists())




class TestRoutineEndToEnd(RunnerCase):
    """The whole spine, with Instagram stubbed: steps assemble, run in order,
    and land in the report without any network."""

    def setUp(self):
        super().setUp()
        import os
        from unittest.mock import patch
        os.environ.update({
            "IG_ACCOUNTS": "anova.autismo,pankeka.app",
            "IG_ANOVA_AUTISMO_USER_ID": "1", "IG_ANOVA_AUTISMO_TOKEN": "t",
            "IG_PANKEKA_APP_USER_ID": "2", "IG_PANKEKA_APP_TOKEN": "t",
        })
        from .channels.instagram import Instagram
        p = patch.object(Instagram, "_request", side_effect=self._route)
        self.addCleanup(p.stop); p.start()

    def _route(self, method, path, **params):
        if method == "POST":
            return {"id": "published-1"}
        if path == "me/conversations":
            return {"data": []}
        if path.endswith("/media"):
            return {"data": []}
        return {}

    def test_daily_runs_every_step_and_reports(self):
        from .routine import daily
        r = self._runner()
        for step in daily(posts={"anova.autismo": {
                "image_url": "https://cdn/x.jpg", "caption": "Rotina visual"}}):
            r.add(step)
        rendered = r.run_all().render()
        self.assertIn("Publicação realizada", rendered)
        self.assertIn("Rotina visual", rendered)
        self.assertIn("Caixa de entrada vazia", rendered)
        self.assertIn("ANOVA.AUTISMO", rendered)
        self.assertIn("PANKEKA.APP", rendered)

    def test_no_post_queued_still_runs_the_checks(self):
        from .routine import daily
        r = self._runner()
        for step in daily():
            r.add(step)
        rendered = r.run_all().render()
        self.assertNotIn("Publicação realizada", rendered)
        self.assertIn("Caixa de entrada vazia", rendered)

    def test_hourly_steps_are_not_once_per_day(self):
        from .routine import hourly
        self.assertTrue(all(not s.once_per_day for s in hourly()))

    def test_post_step_is_once_per_day(self):
        from .routine import instagram_post
        step = instagram_post("anova.autismo", image_url="https://cdn/x.jpg", caption="oi")
        self.assertTrue(step.once_per_day)

if __name__ == "__main__":
    unittest.main(verbosity=2)
