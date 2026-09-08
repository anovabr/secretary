import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from . import deliver


class TestDeliver(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.report = Path(self.tmp.name) / "2026-09-08.txt"
        self.report.write_text("RELATÓRIO", encoding="utf-8")

    def test_without_password_sends_nothing_and_succeeds(self):
        with patch.dict(os.environ, {"SMTP_PASSWORD": ""}), patch("smtplib.SMTP_SSL") as smtp:
            self.assertEqual(deliver.main([str(self.report)]), 0)
        smtp.assert_not_called()

    def test_sends_the_file_as_the_body(self):
        env = {"SMTP_PASSWORD": "x", "SMTP_USER": "contato@anovasaude.org", "REPORT_TO": "me@example.org"}
        with patch.dict(os.environ, env), patch("smtplib.SMTP_SSL") as smtp:
            conn = smtp.return_value.__enter__.return_value
            deliver.main([str(self.report)])
        conn.login.assert_called_once_with("contato@anovasaude.org", "x")
        msg = conn.send_message.call_args[0][0]
        self.assertEqual(msg["To"], "me@example.org")
        self.assertEqual(msg["Subject"], "Relatório da secretária — 2026-09-08")
        self.assertIn("RELATÓRIO", msg.get_content())
