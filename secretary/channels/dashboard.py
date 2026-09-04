"""The task board at anovabr.github.io/dashboard — the routine's source of truth.

The board's **Recurring** sidebar is where the routine is configured. Its
state is an encrypted envelope, `taskboard.json` on the `state` branch of
anovabr/dashboard, which the page rewrites after every change. The secretary
reads it each morning, executes the recurring tasks addressed to it, and
ticks them on the board so the sidebar shows what happened.

The envelope is what the page produces: PBKDF2-SHA256, 250 000 iterations,
over the board password, then AES-256-GCM. The password is DASHBOARD_PASSWORD
in the environment and is never written anywhere else.

Format of a recurring task the secretary executes — the text field, exactly:

    🤖 Publicar @anova.autismo          publish the day's post from media/
    🤖 Responder @anova.autismo         answer messages and comments
    🤖 Painel https://.../admin.html    read an admin panel (not built yet)
    🤖 E-mail contato@anovasaude.org    triage a mailbox (not built yet)

A recurring task without the robot is the board owner's own and is only
listed. A robot task the secretary does not understand is flagged, not
guessed at. Ticking follows the page's own convention: `lastDone` set to
JavaScript's `Date.toDateString()` for the day.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import subprocess
from dataclasses import dataclass
from datetime import date, datetime, timezone

import requests

GH_REPO = "anovabr/dashboard"
GH_BRANCH = "state"
GH_PATH = "taskboard.json"
DEFAULT_URL = f"https://raw.githubusercontent.com/{GH_REPO}/{GH_BRANCH}/{GH_PATH}"
API_URL = f"https://api.github.com/repos/{GH_REPO}/contents/{GH_PATH}"
PBKDF2_ITERATIONS = 250_000

ROBOT = "🤖"

# The page's seed sections; the state only carries the custom ones.
SEED_SECTIONS = {
    "writing": "Writing", "anova": "ANOVA", "rne": "Research & Evaluation",
    "puc": "PUC-Rio", "personal": "Personal", "others": "Others",
}

# The board stamps "done today" with JavaScript's Date.toDateString(),
# e.g. "Fri Sep 04 2026". Matching it exactly is what makes "done" agree.
_DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def day_str(today: date) -> str:
    return f"{_DOW[today.weekday()]} {_MON[today.month - 1]} {today.day:02d} {today.year}"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + f"{datetime.now(timezone.utc).microsecond // 1000:03d}Z"


class DashboardError(RuntimeError):
    pass


# ---------- envelope ----------

def _key(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS, dklen=32)


def decrypt(envelope: dict, password: str) -> dict:
    """The board state inside an envelope the page wrote."""
    from cryptography.exceptions import InvalidTag
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    if envelope.get("enc") != "v1":
        raise DashboardError(f"formato do quadro desconhecido: {envelope.get('enc')!r}")
    key = _key(password, base64.b64decode(envelope["salt"]))
    try:
        plain = AESGCM(key).decrypt(
            base64.b64decode(envelope["iv"]), base64.b64decode(envelope["data"]), None
        )
    except InvalidTag:
        raise DashboardError("senha do quadro incorreta (DASHBOARD_PASSWORD)")
    return json.loads(plain.decode("utf-8"))


def encrypt(state: dict, password: str, *, salt: bytes | None = None, iv: bytes | None = None) -> dict:
    """The inverse, in the page's own format, so the page can read what we write."""
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    salt = salt or os.urandom(16)
    iv = iv or os.urandom(12)
    data = AESGCM(_key(password, salt)).encrypt(iv, json.dumps(state).encode("utf-8"), None)
    return {
        "enc": "v1", "kdf": "PBKDF2-SHA256-250k",
        "salt": base64.b64encode(salt).decode(), "iv": base64.b64encode(iv).decode(),
        "data": base64.b64encode(data).decode(),
    }


# ---------- transport ----------

def _password() -> str:
    password = os.environ.get("DASHBOARD_PASSWORD", "")
    if not password:
        raise DashboardError("DASHBOARD_PASSWORD não configurada")
    return password


def _token() -> str:
    """A GitHub token with write access to the board repo: the environment, else gh's."""
    token = os.environ.get("DASHBOARD_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    try:
        return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True,
                              timeout=15, check=True).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        raise DashboardError("sem token do GitHub para escrever no quadro (DASHBOARD_TOKEN ou gh auth)")


def fetch_envelope(url: str = DEFAULT_URL) -> dict:
    """Read-only, no token: the repository is public."""
    response = requests.get(url, timeout=30)
    if response.status_code != 200:
        raise DashboardError(f"quadro indisponível: HTTP {response.status_code} em {url}")
    try:
        return response.json()
    except ValueError:
        raise DashboardError("quadro indisponível: o arquivo não é JSON")


def load_board(url: str | None = None, password: str | None = None) -> dict:
    """Fetch and decrypt, from the environment unless told otherwise."""
    return decrypt(fetch_envelope(url or os.environ.get("DASHBOARD_URL", DEFAULT_URL)),
                   password or _password())


def update_board(change, *, message: str = "secretary sync") -> dict:
    """Fetch, decrypt, apply `change(state)`, encrypt, write back — the page's own sync.

    The write carries the file's sha, so a concurrent save from the page makes
    GitHub refuse ours rather than silently overwrite it; the caller may retry.
    Returns the state as written.
    """
    password, token = _password(), _token()
    headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}"}
    got = requests.get(API_URL, params={"ref": GH_BRANCH}, headers=headers, timeout=30)
    if got.status_code != 200:
        raise DashboardError(f"quadro indisponível para escrita: HTTP {got.status_code}")
    meta = got.json()
    envelope = json.loads(base64.b64decode(meta["content"]).decode("utf-8"))
    state = decrypt(envelope, password)
    change(state)
    state["savedAt"] = now_iso()
    new = encrypt(state, password, salt=base64.b64decode(envelope["salt"]))
    body = {"message": message, "branch": GH_BRANCH, "sha": meta["sha"],
            "content": base64.b64encode(json.dumps(new).encode("utf-8")).decode()}
    put = requests.put(API_URL, headers=headers, json=body, timeout=30)
    if put.status_code not in (200, 201):
        raise DashboardError(f"o quadro recusou a escrita: HTTP {put.status_code} {put.text[:200]}")
    return state


def tick(task_ids: list[str], today: date | None = None) -> None:
    """Mark tasks done for today on the board, the way the page does."""
    today = today or date.today()
    stamp = day_str(today)

    def change(state: dict) -> None:
        for t in state.get("tasks", []):
            if t.get("id") in task_ids and t.get("lastDone") != stamp:
                t["lastDone"] = stamp
                t["updatedAt"] = now_iso()

    update_board(change, message="secretary: rotinas de hoje")


# ---------- recurring tasks ----------

_JS_DOW = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]   # JavaScript's getDay()

VERBS = {
    "publicar": "publish", "postar": "publish", "post": "publish",
    "responder": "reply", "respond": "reply", "reply": "reply",
    "painel": "panel", "admin": "panel", "panel": "panel",
    "e-mail": "mail", "email": "mail", "mail": "mail",
}


@dataclass(frozen=True)
class Command:
    """What a robot task asks for: an action and its target."""
    action: str      # publish | reply | panel | mail
    target: str      # "anova.autismo", a URL, an e-mail address


def parse(text: str) -> Command | None:
    """`🤖 Publicar @anova.autismo` -> Command("publish", "anova.autismo"); else None."""
    body = text.strip()
    if not body.startswith(ROBOT):
        return None
    words = body[len(ROBOT):].strip().split()
    if len(words) < 2:
        return None
    action = VERBS.get(words[0].lower().rstrip(":"))
    if not action:
        return None
    target = " ".join(words[1:]).strip().lstrip("@")
    return Command(action, target)


@dataclass(frozen=True)
class Routine:
    id: str
    text: str
    section: str        # the board section's title, e.g. "ANOVA"
    project: str        # the task's project tag, e.g. "ANOVA/anova autismo"; may be empty
    rule: str           # "daily", "weekdays", "weekly · Mon", "monthly · 1st"
    ord: int
    due_today: bool
    done_today: bool

    @property
    def mine(self) -> bool:
        """Addressed to the secretary — starts with the robot."""
        return self.text.startswith(ROBOT)

    @property
    def command(self) -> Command | None:
        return parse(self.text)

    @property
    def label(self) -> str:
        return self.text[len(ROBOT):].strip() if self.mine else self.text


def _js_dow(today: date) -> int:
    return (today.weekday() + 1) % 7


def _ordinal(n: int) -> str:
    suffix = "th" if 11 <= n % 100 <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def rule_of(task: dict) -> str:
    repeat = task.get("repeat") or ""
    if repeat == "weekly":
        day = task.get("repeatDay")
        return f"weekly · {_JS_DOW[1 if day is None else day]}"
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
        day = task.get("repeatDay")
        return dow == (1 if day is None else day)
    if repeat == "monthly":
        return today.day == (task.get("repeatDom") or 1)
    return False


def section_titles(state: dict) -> dict[str, str]:
    titles = dict(SEED_SECTIONS)
    for s in state.get("customSections", []) or []:
        titles[s.get("id")] = s.get("title", s.get("id"))
    return titles


def recurring(state: dict, today: date | None = None) -> list[Routine]:
    """Every recurring task still on the board, in the order they are to run."""
    today = today or date.today()
    titles = section_titles(state)
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
            ord=int(t.get("ord") or 0),
            due_today=due_today(t, today),
            done_today=t.get("lastDone") == day_str(today),
        ))
    return sorted(out, key=lambda r: (r.ord, r.text))
