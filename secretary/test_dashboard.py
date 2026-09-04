"""Tests for the task board: envelope, rules, parsing, and the run it produces.
No network — envelopes are made here and the transport is stubbed."""

import os
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path
from unittest.mock import patch

from .channels import dashboard
from .channels.dashboard import Command, day_str, decrypt, due_today, encrypt, parse, recurring

SECTIONS = [{"id": "cms1", "title": "AGEM"}]
MON, SAT, FIRST = date(2026, 9, 7), date(2026, 9, 5), date(2026, 10, 1)


def task(**kw):
    base = {"id": "j1", "sec": "anova", "text": "🤖 Publicar @anova.autismo", "status": "planning"}
    base.update(kw)
    return base


class TestEnvelope(unittest.TestCase):
    def test_round_trip_in_the_pages_format(self):
        env = encrypt({"tasks": [task(repeat="daily")]}, "senha")
        self.assertEqual((env["enc"], env["kdf"]), ("v1", "PBKDF2-SHA256-250k"))
        self.assertEqual(decrypt(env, "senha")["tasks"][0]["id"], "j1")

    def test_wrong_password_is_a_clear_error(self):
        with self.assertRaises(dashboard.DashboardError) as ctx:
            decrypt(encrypt({"tasks": []}, "senha"), "outra")
        self.assertIn("senha", str(ctx.exception))

    def test_missing_password_is_named(self):
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
        self.assertTrue(due_today(task(repeat="weekly"), MON))
        self.assertTrue(due_today(task(repeat="weekly", repeatDay=6), SAT))
        self.assertFalse(due_today(task(repeat="weekly", repeatDay=0), SAT))

    def test_monthly_uses_the_day_of_month(self):
        self.assertTrue(due_today(task(repeat="monthly"), FIRST))
        self.assertFalse(due_today(task(repeat="monthly", repeatDom=5), FIRST))

    def test_day_str_matches_javascript_toDateString(self):
        self.assertEqual(day_str(date(2026, 9, 4)), "Fri Sep 04 2026")


class TestParse(unittest.TestCase):
    def test_robot_verb_target(self):
        self.assertEqual(parse("🤖 Publicar @anova.autismo"), Command("publish", "anova.autismo"))
        self.assertEqual(parse("🤖 Responder @pankeka.app"), Command("reply", "pankeka.app"))
        self.assertEqual(parse("🤖 Painel https://anovasaude.org/admin"), Command("panel", "https://anovasaude.org/admin"))
        self.assertEqual(parse("🤖 E-mail contato@anovasaude.org"), Command("mail", "contato@anovasaude.org"))

    def test_without_the_robot_it_is_not_ours(self):
        self.assertIsNone(parse("Publicar @anova.autismo"))
        self.assertIsNone(parse("Pankeka Google play"))

    def test_robot_with_unknown_verb_or_no_target_is_none(self):
        self.assertIsNone(parse("🤖 Dançar @anova.autismo"))
        self.assertIsNone(parse("🤖 Publicar"))


class TestRecurring(unittest.TestCase):
    def test_lists_live_recurring_tasks_in_ord_order_with_titles(self):
        state = {"customSections": SECTIONS, "tasks": [
            task(id="b", repeat="daily", ord=2, sec="cms1", text="Ler e-mails"),
            task(id="a", repeat="daily", ord=1),
            task(id="x", repeat="daily", status="gone"),
            task(id="y"),
        ]}
        got = recurring(state, MON)
        self.assertEqual([r.id for r in got], ["a", "b"])
        self.assertEqual([r.section for r in got], ["ANOVA", "AGEM"])
        self.assertTrue(got[0].mine); self.assertFalse(got[1].mine)
        self.assertEqual(got[0].label, "Publicar @anova.autismo")

    def test_done_today_means_ticked_with_todays_stamp(self):
        state = {"tasks": [task(id="a", repeat="daily", lastDone="Mon Sep 07 2026"),
                           task(id="b", repeat="daily", lastDone="Sun Sep 06 2026")]}
        self.assertEqual({r.id: r.done_today for r in recurring(state, MON)}, {"a": True, "b": False})


class TestRunFromBoard(unittest.TestCase):
    """The morning run is what the board says, in board order, ticked when done."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        d = Path(self.tmp.name) / "anova.autismo" / "post-01"; d.mkdir(parents=True)
        (d / "1.png").write_bytes(b"x"); (d / "2.png").write_bytes(b"x")
        os.environ.update({"IG_ACCOUNTS": "anova.autismo,pankeka.app",
                           "IG_ANOVA_AUTISMO_TOKEN": "t", "IG_PANKEKA_APP_TOKEN": "t"})
        from .channels.instagram import Instagram
        p = patch.object(Instagram, "_request", side_effect=self._route); self.addCleanup(p.stop); p.start()

    def _route(self, method, path, **params):
        if method == "POST":
            return {"id": "published-1"}
        if "status_code" in params.get("fields", ""):
            return {"status_code": "FINISHED"}
        if path == "me":
            return {"id": "999"}
        return {"data": []}

    BOARD = {"tasks": [
        task(id="t1", ord=1, repeat="daily", text="🤖 Publicar @anova.autismo"),
        task(id="t2", ord=2, repeat="daily", text="🤖 Responder @anova.autismo"),
        task(id="t3", ord=3, repeat="daily", text="🤖 Painel https://anovasaude.org/admin"),
        task(id="t4", ord=4, repeat="daily", text="🤖 Publicar @pankeka.app"),     # no media
        task(id="t5", ord=5, repeat="daily", text="🤖 Voar @lua"),
        task(id="t6", ord=6, repeat="daily", text="Pankeka Google play", sec="others"),
        task(id="t7", ord=7, repeat="weekly", repeatDay=3, text="🤖 Publicar @pankeka.app"),  # not Monday
    ]}

    def _run(self, board, dry_run=True):
        from .report import Report
        from .routine import from_board
        from .runner import DayState, Runner

        ticked = []
        runner = Runner(Report(datetime(2026, 9, 7, 7, 0)), DayState(Path(self.tmp.name) / "state.json", today=MON),
                        dry_run=dry_run)
        for step in from_board(board, MON, root=self.tmp.name):
            runner.add(step)
        with patch.object(dashboard, "tick", side_effect=lambda ids, today=None: ticked.extend(ids)):
            text = runner.run_all().render()
        return text, ticked

    def test_steps_follow_the_board_and_report_what_is_missing(self):
        text, _ = self._run(self.BOARD)
        self.assertIn("6 rotinas previstas para hoje", text)
        self.assertIn("Publicação realizada", text)                     # t1
        self.assertIn("Caixa de entrada vazia", text)                   # t2
        self.assertIn("O leitor de painéis ainda não existe", text)  # t3
        self.assertIn("Sem post preparado", text)                       # t4
        self.assertIn("Não entendi esta rotina do quadro", text)        # t5
        self.assertIn("rotina sua ainda não marcada", text)             # t6
        self.assertNotIn("weekly", text)                                # t7 not due

    def test_dry_run_ticks_nothing_and_live_run_ticks_what_succeeded(self):
        _, ticked = self._run(self.BOARD, dry_run=True)
        self.assertEqual(ticked, [])
        _, ticked = self._run(self.BOARD, dry_run=False)
        self.assertEqual(ticked, ["t1", "t2"])

    def test_already_ticked_robot_tasks_are_not_run_again(self):
        board = {"tasks": [task(id="t1", ord=1, repeat="daily", lastDone="Mon Sep 07 2026")]}
        text, ticked = self._run(board, dry_run=False)
        self.assertNotIn("Publicação realizada", text)
        self.assertIn("✓ 🤖 [ANOVA] Publicar @anova.autismo", text)
        self.assertEqual(ticked, [])

    def test_board_with_no_robot_tasks_runs_the_builtin_list(self):
        board = {"tasks": [task(id="t6", ord=6, repeat="daily", text="Pankeka Google play", sec="others")]}
        text, ticked = self._run(board, dry_run=False)
        self.assertIn("usando a lista embutida", text)
        self.assertIn("Publicação realizada", text)
        self.assertEqual(ticked, [])

    def test_unreadable_board_falls_back_to_the_builtin_list(self):
        from .routine import daily
        with patch.object(dashboard, "load_board", side_effect=dashboard.DashboardError("HTTP 500")):
            keys = [s.key for s in daily(MON, root=self.tmp.name)]
        self.assertEqual(keys[0], "board:unavailable")
        self.assertIn("post:anova.autismo", keys)
        self.assertIn("messages:pankeka.app", keys)


if __name__ == "__main__":
    unittest.main()
