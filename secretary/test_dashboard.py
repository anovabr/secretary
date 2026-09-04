"""Tests for reading the task board. No network: envelopes are made here."""

import unittest
from datetime import date

from .channels import dashboard
from .channels.dashboard import Routine, day_str, decrypt, due_today, encrypt, recurring

SECTIONS = [{"id": "anova", "title": "ANOVA"}, {"id": "others", "title": "Others"}]

MON, SAT, FIRST = date(2026, 9, 7), date(2026, 9, 5), date(2026, 10, 1)


def task(**kw):
    base = {"id": "j1", "sec": "anova", "text": "Post instagram", "status": "now"}
    base.update(kw)
    return base


class TestEnvelope(unittest.TestCase):
    def test_round_trip_in_the_pages_format(self):
        env = encrypt({"tasks": [task(repeat="daily")], "sections": SECTIONS}, "senha")
        self.assertEqual(env["enc"], "v1")
        self.assertEqual(env["kdf"], "PBKDF2-SHA256-250k")
        self.assertEqual(decrypt(env, "senha")["tasks"][0]["text"], "Post instagram")

    def test_wrong_password_is_a_clear_error(self):
        env = encrypt({"tasks": []}, "senha")
        with self.assertRaises(dashboard.DashboardError) as ctx:
            decrypt(env, "outra")
        self.assertIn("senha", str(ctx.exception))

    def test_missing_password_says_where_it_goes(self):
        import os
        from unittest.mock import patch
        with patch.dict(os.environ, {"DASHBOARD_PASSWORD": ""}):
            with self.assertRaises(dashboard.DashboardError) as ctx:
                dashboard.load_board()
        self.assertIn("DASHBOARD_PASSWORD", str(ctx.exception))


class TestRules(unittest.TestCase):
    def test_daily_is_always_due(self):
        self.assertTrue(due_today(task(repeat="daily"), SAT))

    def test_weekdays_skip_the_weekend(self):
        self.assertTrue(due_today(task(repeat="weekdays"), MON))
        self.assertFalse(due_today(task(repeat="weekdays"), SAT))

    def test_weekly_counts_sunday_as_zero_like_javascript(self):
        self.assertTrue(due_today(task(repeat="weekly", repeatDay=1), MON))
        self.assertTrue(due_today(task(repeat="weekly"), MON))          # default Monday
        self.assertTrue(due_today(task(repeat="weekly", repeatDay=6), SAT))
        self.assertFalse(due_today(task(repeat="weekly", repeatDay=0), SAT))

    def test_monthly_uses_the_day_of_month(self):
        self.assertTrue(due_today(task(repeat="monthly"), FIRST))
        self.assertFalse(due_today(task(repeat="monthly", repeatDom=5), FIRST))

    def test_day_str_matches_javascript_toDateString(self):
        self.assertEqual(day_str(date(2026, 9, 4)), "Fri Sep 04 2026")


class TestRecurring(unittest.TestCase):
    def test_lists_only_live_recurring_tasks_with_section_titles(self):
        state = {"sections": SECTIONS, "tasks": [
            task(id="a", repeat="daily", proj="anova autismo"),
            task(id="b", repeat="daily", status="gone"),
            task(id="c"),                                       # not recurring
            task(id="d", sec="others", repeat="monthly", repeatDom=1, text="Pankeka Google play"),
        ]}
        got = recurring(state, MON)
        self.assertEqual([r.id for r in got], ["a", "d"])
        self.assertEqual(got[0].section, "ANOVA")
        self.assertEqual(got[0].label, "anova autismo / Post instagram")
        self.assertEqual(got[1].rule, "monthly · 1st")
        self.assertTrue(got[0].due_today)
        self.assertFalse(got[1].due_today)

    def test_done_today_means_ticked_with_todays_stamp(self):
        state = {"tasks": [task(id="a", repeat="daily", lastDone="Mon Sep 07 2026"),
                           task(id="b", repeat="daily", lastDone="Sun Sep 06 2026")]}
        got = {r.id: r.done_today for r in recurring(state, MON)}
        self.assertEqual(got, {"a": True, "b": False})


class TestStep(unittest.TestCase):
    def test_reports_due_routines_and_flags_the_unticked(self):
        from datetime import datetime
        from unittest.mock import patch

        from .report import Report
        from .routine import board_routines
        from .runner import StepContext

        state = {"sections": SECTIONS, "tasks": [
            task(id="a", repeat="daily", text="Post instagram", lastDone=day_str(date.today())),
            task(id="b", repeat="daily", text="Admin anovasaude"),
        ]}
        report = Report(datetime.now())
        step = board_routines()
        with patch.object(dashboard, "load_board", return_value=state):
            step.run(StepContext(report, report.section(step.title), dry_run=True))
        text = report.render()
        self.assertIn("2 rotinas previstas para hoje", text)
        self.assertIn("✓ [ANOVA] Post instagram", text)
        self.assertIn("· [ANOVA] Admin anovasaude", text)
        self.assertIn("1 rotina do quadro ainda não marcada", text)


if __name__ == "__main__":
    unittest.main()
