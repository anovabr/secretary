"""Tests for the panel readers, on temporary databases shaped like the real ones."""

import os
import sqlite3
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from .channels import panels
from .channels.panels import AnovaSaude, AutismoSaude, panel_for, read_panel

ANOVA_SCHEMA = """
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, role TEXT DEFAULT 'person',
  professional_type TEXT, full_name TEXT, created_at TEXT DEFAULT (datetime('now')));
CREATE TABLE professional_profiles (user_id INTEGER PRIMARY KEY, crp_or_registration TEXT);
CREATE TABLE test_results (id INTEGER PRIMARY KEY AUTOINCREMENT, test_key TEXT, platform TEXT,
  interpretation_level TEXT, critical INTEGER DEFAULT 0, created_at TEXT DEFAULT (datetime('now')));
CREATE TABLE patients (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT DEFAULT (datetime('now')));
"""

AUTISMO_SCHEMA = """
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, name TEXT, plan TEXT DEFAULT 'free',
  created_at TEXT DEFAULT (datetime('now')));
CREATE TABLE instrument_starts (id INTEGER PRIMARY KEY AUTOINCREMENT, session_token TEXT, instrument_id TEXT,
  started_at TEXT DEFAULT (datetime('now')));
CREATE TABLE test_attempts (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, session_token TEXT,
  instrument_id TEXT, result TEXT, created_at TEXT DEFAULT (datetime('now')));
CREATE TABLE payments (id INTEGER PRIMARY KEY AUTOINCREMENT, plan TEXT, status TEXT, amount_charged REAL,
  created_at TEXT DEFAULT (datetime('now')));
"""


class PanelCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.state = Path(self.tmp.name) / "marks.json"

    def make_db(self, name, schema):
        path = Path(self.tmp.name) / name
        with sqlite3.connect(path) as c:
            c.executescript(schema)
        return str(path)


class TestAnovaSaude(PanelCase):
    def setUp(self):
        super().setUp()
        self.db = self.make_db("anova.db", ANOVA_SCHEMA)
        with sqlite3.connect(self.db) as c:
            c.execute("INSERT INTO users (role, full_name) VALUES ('person', 'Ana')")
            c.execute("INSERT INTO users (role, professional_type, full_name) VALUES ('professional', 'psychologist', 'Bia')")
            c.execute("INSERT INTO users (role, professional_type, full_name) VALUES ('professional', 'doctor', 'Caio')")
            c.execute("INSERT INTO professional_profiles VALUES (3, 'CRM 123')")
            c.execute("INSERT INTO test_results (test_key, platform) VALUES ('rabesp-a', 'public')")
            c.execute("INSERT INTO test_results (test_key, platform, critical) VALUES ('rabesp-a', 'professional', 1)")
            c.execute("INSERT INTO test_results (test_key, platform) VALUES ('faux-pas', 'public')")
        patch.object(AnovaSaude, "db", self.db).start(); self.addCleanup(patch.stopall)

    def test_first_run_reports_the_last_day_and_holds_the_pro_without_a_number(self):
        f = read_panel("https://anovasaude.org/admin", state_path=self.state)
        done = dict(f.done); att = dict(f.attention)
        self.assertIn("3 cadastros novos", done)
        self.assertIn("1 pessoas, 2 profissionais", done["3 cadastros novos"])
        self.assertIn("Ana\nBia — psychologist\nCaio — doctor", done["3 cadastros novos"])
        self.assertIn("3 avaliações realizadas", done)
        self.assertIn("rabesp-a 2, faux-pas 1", done["3 avaliações realizadas"])
        self.assertEqual(att["1 profissional sem número de conselho"], "Bia — psychologist")
        self.assertIn("1 resultado marcado como crítico", att)

    def test_second_run_reports_only_what_is_new(self):
        read_panel("https://anovasaude.org/admin", state_path=self.state)
        with sqlite3.connect(self.db) as c:
            c.execute("INSERT INTO users (role, full_name) VALUES ('person', 'Duda')")
        f = read_panel("https://anovasaude.org/admin", state_path=self.state)
        done = dict(f.done)
        self.assertIn("1 cadastro novo", done)
        self.assertIn("Nenhuma avaliação realizada", done)

    def test_dry_run_does_not_advance_the_watermark(self):
        read_panel("https://anovasaude.org/admin", state_path=self.state, advance=False)
        self.assertFalse(self.state.exists())
        f = read_panel("https://anovasaude.org/admin", state_path=self.state)
        self.assertIn("3 cadastros novos", dict(f.done))


class TestAutismoSaude(PanelCase):
    def test_counts_signups_tests_and_payments(self):
        db = self.make_db("users.db", AUTISMO_SCHEMA)
        with sqlite3.connect(db) as c:
            c.execute("INSERT INTO users (name, plan) VALUES ('Eva', 'free')")
            c.execute("INSERT INTO instrument_starts (session_token, instrument_id) VALUES ('s1', 'rabesp-a')")
            c.execute("INSERT INTO instrument_starts (session_token, instrument_id) VALUES ('s2', 'rabesp-a')")
            c.execute("INSERT INTO test_attempts (session_token, instrument_id, result) VALUES ('s1', 'rabesp-a', '{}')")
            c.execute("INSERT INTO payments (plan, status, amount_charged) VALUES ('premium', 'approved', 29.9)")
            c.execute("INSERT INTO payments (plan, status, amount_charged) VALUES ('premium', 'pending', 29.9)")
        with patch.object(AutismoSaude, "db", db):
            f = read_panel("https://autismo.anovasaude.org/admin.html", state_path=self.state)
        done = dict(f.done)
        self.assertEqual(done["1 cadastro novo"], "Eva — free")
        self.assertIn("1 teste concluído, 2 iniciados", done)
        self.assertIn("R$ 29.90", done["1 pagamento aprovado"])
        self.assertEqual(f.attention, [])


class TestLookup(unittest.TestCase):
    def test_urls_are_matched_loosely(self):
        self.assertIsInstance(panel_for("https://anovasaude.org/admin/"), AnovaSaude)
        self.assertIsInstance(panel_for("http://www.autismo.anovasaude.org/admin.html"), AutismoSaude)
        self.assertIsNone(panel_for("https://outro.site/admin"))

    def test_unknown_panel_on_the_board_is_flagged_not_guessed(self):
        from .channels import dashboard
        from .report import Report
        from .routine import from_board
        from .runner import StepContext

        board = {"tasks": [{"id": "p9", "sec": "anova", "text": "🤖 Painel https://outro.site/admin",
                            "status": "planning", "repeat": "daily", "ord": 1}]}
        steps = from_board(board)
        report = Report(datetime.now())
        for step in steps:
            step.run(StepContext(report, report.section(step.title), dry_run=True))
        text = report.render()
        self.assertIn("Não entendi esta rotina do quadro", text)
        self.assertIn("Painéis conhecidos", text)


if __name__ == "__main__":
    unittest.main()
