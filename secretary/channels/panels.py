"""The admin panels — read straight from their databases, by the URL on the board.

`🤖 Painel <url>` on the board names a panel. The panels that live on this
VPS are read from their SQLite files, read-only, with no login: nothing to
expire and nothing an administrator's session could do by accident. A URL
nobody has taught the secretary is reported as such, so adding a site to
the board is safe — it shows up as "ensine-me" until an adapter exists here.

Each morning reports only what is new since the last real run: a watermark
per table (the highest id seen) is kept in .secretary-panels.json. A dry run
reads but never advances the watermark. The first run reports the last 24h.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

STATE_FILE = ".secretary-panels.json"


@dataclass
class Findings:
    """What a panel had to say: lines for the report, and what needs a person."""
    done: list[tuple[str, str]] = field(default_factory=list)       # (what, detail)
    attention: list[tuple[str, str]] = field(default_factory=list)  # (what, detail)
    marks: dict[str, int] = field(default_factory=dict)             # table -> highest id seen

    def feito(self, what: str, detail: str = "") -> None:
        self.done.append((what, detail))

    def atencao(self, what: str, detail: str = "") -> None:
        self.attention.append((what, detail))


def _plural(n: int, one: str, many: str) -> str:
    return f"{n} {one if n == 1 else many}"


def _count_by(rows, key) -> str:
    counts: dict[str, int] = {}
    for r in rows:
        k = r[key] or "?"
        counts[k] = counts.get(k, 0) + 1
    return ", ".join(f"{k} {v}" for k, v in sorted(counts.items(), key=lambda kv: -kv[1]))


class Panel:
    """One admin site. Subclasses know its tables."""

    name = ""
    db: str = ""

    def __init__(self, db: str | None = None):
        if db:
            self.db = db

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(f"file:{self.db}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        return conn

    def _new(self, conn, table: str, marks: dict, order_col: str = "id", since_col: str = "created_at",
             where: str = "", cols: str = "*") -> list[sqlite3.Row]:
        """Rows added since the watermark; on the first run, the last 24 hours."""
        extra = f" AND ({where})" if where else ""
        if table in marks:
            sql = f"SELECT {cols} FROM {table} WHERE {order_col} > ?{extra} ORDER BY {order_col}"
            return conn.execute(sql, (marks[table],)).fetchall()
        sql = f"SELECT {cols} FROM {table} WHERE {since_col} >= datetime('now', '-1 day'){extra} ORDER BY {order_col}"
        return conn.execute(sql).fetchall()

    def _mark(self, conn, table: str, findings: Findings, order_col: str = "id") -> None:
        top = conn.execute(f"SELECT MAX({order_col}) FROM {table}").fetchone()[0]
        findings.marks[table] = int(top or 0)

    def read(self, marks: dict) -> Findings:
        raise NotImplementedError


class AnovaSaude(Panel):
    """anovasaude.org/admin — people, professionals, tests, patients."""

    name = "anovasaude.org"
    db = "/opt/anovasaude/admin/anova.db"

    def read(self, marks: dict) -> Findings:
        f = Findings()
        with self.connect() as conn:
            users = self._new(conn, "users", marks,
                              cols="id, full_name, role, professional_type, created_at")
            people = [u for u in users if u["role"] == "person"]
            pros = [u for u in users if u["role"] == "professional"]
            if users:
                names = [f"{u['full_name'] or '(sem nome)'}" + (f" — {u['professional_type']}" if u["role"] == "professional" else "")
                         for u in users[:10]]
                f.feito(_plural(len(users), "cadastro novo", "cadastros novos"),
                        f"{len(people)} pessoas, {len(pros)} profissionais\n" + "\n".join(names)
                        + (f"\n… e mais {len(users) - 10}" if len(users) > 10 else ""))
            else:
                f.feito("Nenhum cadastro novo")
            missing = [u for u in pros if not conn.execute(
                "SELECT crp_or_registration FROM professional_profiles WHERE user_id = ?", (u["id"],)
            ).fetchone() or not (conn.execute(
                "SELECT crp_or_registration FROM professional_profiles WHERE user_id = ?", (u["id"],)
            ).fetchone()[0] or "").strip()]
            if missing:
                f.atencao(_plural(len(missing), "profissional sem número de conselho",
                                  "profissionais sem número de conselho"),
                          "\n".join(f"{u['full_name'] or '(sem nome)'} — {u['professional_type']}" for u in missing[:8]))
            self._mark(conn, "users", f)

            tests = self._new(conn, "test_results", marks,
                              cols="id, test_key, platform, interpretation_level, critical, created_at")
            if tests:
                f.feito(_plural(len(tests), "avaliação realizada", "avaliações realizadas"),
                        _count_by(tests, "test_key") + f"\nplataforma: {_count_by(tests, 'platform')}")
                critical = [t for t in tests if t["critical"]]
                if critical:
                    f.atencao(_plural(len(critical), "resultado marcado como crítico",
                                      "resultados marcados como críticos"),
                              _count_by(critical, "test_key"))
            else:
                f.feito("Nenhuma avaliação realizada")
            self._mark(conn, "test_results", f)

            patients = self._new(conn, "patients", marks, cols="id, created_at")
            if patients:
                f.feito(_plural(len(patients), "paciente novo cadastrado por profissional",
                                "pacientes novos cadastrados por profissionais"))
            self._mark(conn, "patients", f)
        return f


class AutismoSaude(Panel):
    """autismo.anovasaude.org/admin.html — the screening site."""

    name = "autismo.anovasaude.org"
    db = "/opt/autismosaude/users.db"

    def read(self, marks: dict) -> Findings:
        f = Findings()
        with self.connect() as conn:
            users = self._new(conn, "users", marks, cols="id, name, plan, created_at")
            if users:
                names = [f"{u['name'] or '(sem nome)'} — {u['plan']}" for u in users[:10]]
                f.feito(_plural(len(users), "cadastro novo", "cadastros novos"),
                        "\n".join(names) + (f"\n… e mais {len(users) - 10}" if len(users) > 10 else ""))
            else:
                f.feito("Nenhum cadastro novo")
            self._mark(conn, "users", f)

            starts = self._new(conn, "instrument_starts", marks, since_col="started_at",
                               cols="id, instrument_id, started_at")
            attempts = self._new(conn, "test_attempts", marks, cols="id, instrument_id, user_id, created_at")
            if attempts or starts:
                f.feito(_plural(len(attempts), "teste concluído", "testes concluídos")
                        + f", {len(starts)} iniciados",
                        (f"concluídos: {_count_by(attempts, 'instrument_id')}" if attempts else "")
                        + (f"\niniciados: {_count_by(starts, 'instrument_id')}" if starts else ""))
            else:
                f.feito("Nenhum teste iniciado ou concluído")
            self._mark(conn, "instrument_starts", f)
            self._mark(conn, "test_attempts", f)

            self._ads(conn, f)

            try:
                paid = self._new(conn, "payments", marks, where="status = 'approved'",
                                 cols="id, plan, amount_charged, created_at")
                if paid:
                    total = sum(float(p["amount_charged"] or 0) for p in paid)
                    f.feito(_plural(len(paid), "pagamento aprovado", "pagamentos aprovados"),
                            f"R$ {total:,.2f} — {_count_by(paid, 'plan')}")
                self._mark(conn, "payments", f)
            except sqlite3.OperationalError as exc:      # the payments table may change shape
                f.atencao("Não consegui ler os pagamentos", str(exc))
        return f

    # Paid boosts link to /anuncio, which lands with utm_source=anuncio; the site keeps that
    # tag on the visit (site_visits) and, since 2026-11-07, on each finished test
    # (test_attempts.utm_source). Windows are by date, not watermark: the same numbers
    # every time they are read, so a dry run changes nothing.
    AD_SOURCE = "anuncio"
    BASELINE_DAYS = 14

    def _ads(self, conn, f: Findings) -> None:
        try:
            first = conn.execute("SELECT MIN(created_at) FROM site_visits WHERE utm_source = ?",
                                 (self.AD_SOURCE,)).fetchone()[0]
        except sqlite3.OperationalError:
            return                                   # no visit tracking in this database
        if not first:
            return                                   # no ad has brought anyone yet

        def one(sql, *args):
            return conn.execute(sql, args).fetchone()[0] or 0

        day = "created_at >= datetime('now', '-1 day')"
        visits_day = one(f"SELECT COUNT(*) FROM site_visits WHERE utm_source = ? AND {day}", self.AD_SOURCE)
        visits_all = one("SELECT COUNT(*) FROM site_visits WHERE utm_source = ?", self.AD_SOURCE)
        try:
            tests_day = one(f"SELECT COUNT(DISTINCT session_token) FROM test_attempts "
                            f"WHERE utm_source = ? AND {day}", self.AD_SOURCE)
            tests_all = one("SELECT COUNT(DISTINCT session_token) FROM test_attempts WHERE utm_source = ?",
                            self.AD_SOURCE)
            tests = (f", {_plural(tests_day, 'rastreio concluído', 'rastreios concluídos')}",
                     f", {_plural(tests_all, 'rastreio', 'rastreios')}")
        except sqlite3.OperationalError:             # site not yet restarted with the tag
            tests = ("", "")

        # The whole site against the fortnight before the first ad visit: catches people who
        # saw the ad and came later by the bio or by typing the address.
        site_day = one(f"SELECT COUNT(*) FROM site_visits WHERE {day}")
        done_day = one(f"SELECT COUNT(DISTINCT session_token) FROM test_attempts WHERE {day}")
        window = f"created_at >= datetime(?, '-{self.BASELINE_DAYS} days') AND created_at < ?"
        site_base = one(f"SELECT COUNT(*) FROM site_visits WHERE {window}", first, first) / self.BASELINE_DAYS
        done_base = one(f"SELECT COUNT(DISTINCT session_token) FROM test_attempts WHERE {window}",
                        first, first) / self.BASELINE_DAYS

        f.feito(f"Anúncio: {_plural(visits_day, 'visita', 'visitas')} nas últimas 24h{tests[0]}",
                f"desde {first[8:10]}/{first[5:7]}: {_plural(visits_all, 'visita', 'visitas')}{tests[1]}\n"
                f"site inteiro nas últimas 24h: {site_day} visitas, {done_day} rastreios — "
                f"nos {self.BASELINE_DAYS} dias antes do anúncio, média de "
                f"{site_base:.0f} visitas e {done_base:.1f} rastreios por dia")


PANELS: dict[str, type[Panel]] = {
    "anovasaude.org/admin": AnovaSaude,
    "autismo.anovasaude.org/admin.html": AutismoSaude,
}


def _normalise(url: str) -> str:
    u = url.strip().lower()
    for prefix in ("https://", "http://", "www."):
        if u.startswith(prefix):
            u = u[len(prefix):]
    return u.rstrip("/")


def panel_for(url: str) -> Panel | None:
    cls = PANELS.get(_normalise(url))
    return cls() if cls else None


# ---------- watermarks ----------

def load_marks(path: str | Path = STATE_FILE) -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except ValueError:
        return {}


def save_marks(url: str, marks: dict, path: str | Path = STATE_FILE) -> None:
    p = Path(path)
    data = load_marks(p)
    data[_normalise(url)] = marks
    p.write_text(json.dumps(data, indent=1), encoding="utf-8")


def read_panel(url: str, *, state_path: str | Path = STATE_FILE, advance: bool = True) -> Findings:
    """Read one panel since its last real run; advance the watermark unless told not to."""
    panel = panel_for(url)
    if panel is None:
        raise KeyError(url)
    findings = panel.read(load_marks(state_path).get(_normalise(url), {}))
    if advance:
        save_marks(url, findings.marks, state_path)
    return findings
