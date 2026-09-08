"""Send the day's report by e-mail, from contato@anovasaude.org (Titan SMTP).

    python3 -m secretary.deliver reports/2026-09-08.txt

Needs SMTP_PASSWORD in the environment; SMTP_USER defaults to
contato@anovasaude.org and REPORT_TO to the same address. Without a
password it exits quietly, so the run is never blocked by delivery.
"""

from __future__ import annotations

import os
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

SMTP_HOST, SMTP_PORT = "smtp.titan.email", 465


def send(report: str, subject: str, *, user: str, password: str, to: str) -> None:
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = user, to, subject
    msg.set_content(report)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30) as smtp:
        smtp.login(user, password)
        smtp.send_message(msg)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print("uso: python3 -m secretary.deliver reports/AAAA-MM-DD.txt", file=sys.stderr)
        return 2
    password = os.environ.get("SMTP_PASSWORD", "")
    if not password:
        return 0
    path = Path(argv[0])
    user = os.environ.get("SMTP_USER", "contato@anovasaude.org")
    to = os.environ.get("REPORT_TO", user)
    send(path.read_text(encoding="utf-8"), f"Relatório da secretária — {path.stem}",
         user=user, password=password, to=to)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
