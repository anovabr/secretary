"""The task board at anovabr.github.io/dashboard — read-only.

The board is the source of truth for what recurs. Its state is an encrypted
envelope, `taskboard.json` on the `state` branch of anovabr/dashboard, which
the page writes after every change. Reading it here means the routine can be
changed on the board and the secretary sees it the next morning.

The envelope is what the page produces: PBKDF2-SHA256, 250 000 iterations,
over the board password, then AES-256-GCM. The password lives in the
environment as DASHBOARD_PASSWORD and is never written anywhere else.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import date

import requests

DEFAULT_URL = "https://raw.githubusercontent.com/anovabr/dashboard/state/taskboard.json"
PBKDF2_ITERATIONS = 250_000

# The board stamps "done today" with JavaScript's Date.toDateString(),
# e.g. "Fri Sep 04 2026". Matching it exactly is what makes "done" agree.
_DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def day_str(today: date) -> str:
    return f"{_DOW[today.weekday()]} {_MON[today.month - 1]} {today.day:02d} {today.year}"


class DashboardError(RuntimeError):
    pass


# ---------- envelope ----------

def fetch_envelope(url: str = DEFAULT_URL) -> dict:
    response = requests.get(url, timeout=30)
    if response.status_code != 200:
        raise DashboardError(f"quadro indisponível: HTTP {response.status_code} em {url}")
    try:
        return response.json()
    except ValueError:
        raise DashboardError("quadro indisponível: o arquivo não é JSON")


def decrypt(envelope: dict, password: str) -> dict:
    """The board state inside an envelope the page wrote."""
    from cryptography.exceptions import InvalidTag
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    if envelope.get("enc") != "v1":
        raise DashboardError(f"formato do quadro desconhecido: {envelope.get('enc')!r}")
    key = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), base64.b64decode(envelope["salt"]),
        PBKDF2_ITERATIONS, dklen=32,
    )
    try:
        plain = AESGCM(key).decrypt(
            base64.b64decode(envelope["iv"]), base64.b64decode(envelope["data"]), None
        )
    except InvalidTag:
        raise DashboardError("senha do quadro incorreta (DASHBOARD_PASSWORD)")
    return json.loads(plain.decode("utf-8"))


def encrypt(state: dict, password: str, *, salt: bytes | None = None, iv: bytes | None = None) -> dict:
    """The inverse, in the page's own format. Used by the tests; the secretary never writes."""
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    salt = salt or os.urandom(16)
    iv = iv or os.urandom(12)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS, dklen=32)
    data = AESGCM(key).encrypt(iv, json.dumps(state).encode("utf-8"), None)
    return {
        "enc": "v1", "kdf": "PBKDF2-SHA256-250k",
        "salt": base64.b64encode(salt).decode(), "iv": base64.b64encode(iv).decode(),
        "data": base64.b64encode(data).decode(),
    }


def load_board(url: str | None = None, password: str | None = None) -> dict:
    """Fetch and decrypt, from the environment unless told otherwise."""
    password = password or os.environ.get("DASHBOARD_PASSWORD", "")
    if not password:
        raise DashboardError("DASHBOARD_PASSWORD não configurada — a senha do quadro vai no .env")
    return decrypt(fetch_envelope(url or os.environ.get("DASHBOARD_URL", DEFAULT_URL)), password)


# ---------- recurring tasks ----------

@dataclass(frozen=True)
class Routine:
    id: str
    text: str
    section: str        # the board section's title, e.g. "ANOVA"
    project: str        # the task's project tag, e.g. "anova autismo"; may be empty
    rule: str           # "daily", "weekdays", "weekly · Mon", "monthly · 1st"
    due_today: bool
    done_today: bool

    @property
    def label(self) -> str:
        return f"{self.project} / {self.text}" if self.project else self.text


_JS_DOW = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]   # JavaScript's getDay()


def _js_dow(today: date) -> int:
    return (today.weekday() + 1) % 7


def _ordinal(n: int) -> str:
    suffix = "th" if 11 <= n % 100 <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def rule_of(task: dict) -> str:
    repeat = task.get("repeat") or ""
    if repeat == "weekly":
        return f"weekly · {_JS_DOW[task.get('repeatDay') if task.get('repeatDay') is not None else 1]}"
    if repeat == "monthly":
        return f"monthly · {_ordinal(task.get('repeatDom') or 1)}"
    return repeat


def due_today(task: dict, today: date) -> bool:
    """The board's own rule, line for line."""
    repeat = task.get("repeat")
    if not repeat:
        return False
    dow = _js_dow(today)
    if repeat == "daily":
        return True
    if repeat == "weekdays":
        return 1 <= dow <= 5
    if repeat == "weekly":
        return dow == (task.get("repeatDay") if task.get("repeatDay") is not None else 1)
    if repeat == "monthly":
        return today.day == (task.get("repeatDom") or 1)
    return False


def recurring(state: dict, today: date | None = None) -> list[Routine]:
    """Every recurring task still on the board, in board order."""
    today = today or date.today()
    titles = {s.get("id"): s.get("title", s.get("id")) for s in state.get("sections", [])}
    out = []
    for t in state.get("tasks", []):
        if not t.get("repeat") or t.get("status") in ("gone", "archived"):
            continue
        out.append(Routine(
            id=t.get("id", ""),
            text=(t.get("text") or "").strip(),
            section=titles.get(t.get("sec"), t.get("sec") or ""),
            project=(t.get("proj") or "").strip(),
            rule=rule_of(t),
            due_today=due_today(t, today),
            done_today=t.get("lastDone") == day_str(today),
        ))
    return out
