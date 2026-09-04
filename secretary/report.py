"""The end-of-run report.

A real secretary does not hand over a log. She says what she did, what she
could not do and why, and what now needs you — in that order, briefly.

The run appends entries as it goes; nothing is composed at the end from
memory, so a crash halfway still leaves a truthful partial report.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
         "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

DIAS = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
        "sexta-feira", "sábado", "domingo"]


class Status(Enum):
    FEITO = "✓"       # completed, nothing owed
    ATENCAO = "!"     # done as far as possible, but you need to look
    FALHOU = "✗"      # could not be done
    PULADO = "–"      # not applicable today


@dataclass
class Entry:
    status: Status
    what: str
    detail: str | None = None
    link: str | None = None
    at: datetime = field(default_factory=datetime.now)


@dataclass
class Section:
    title: str
    entries: list[Entry] = field(default_factory=list)


class Report:
    """Collects what happened, then renders it as a briefing."""

    def __init__(self, when: datetime | None = None, *, titulo: str = "Relatório da secretária"):
        self.when = when or datetime.now()
        self.titulo = titulo
        self.sections: list[Section] = []

    # ---------- collecting ----------

    def section(self, title: str) -> Section:
        """Get the section with this title, creating it once.

        Several steps write under one heading — posting, messages and comments
        all belong to the same account — so asking twice must return the same
        section rather than repeating the heading.
        """
        for existing in self.sections:
            if existing.title == title:
                return existing
        section = Section(title)
        self.sections.append(section)
        return section

    def _add(self, section: Section, status: Status, what: str,
             detail: str | None = None, link: str | None = None) -> None:
        section.entries.append(Entry(status, what, detail, link))

    def feito(self, section: Section, what: str, detail: str | None = None,
              link: str | None = None) -> None:
        self._add(section, Status.FEITO, what, detail, link)

    def atencao(self, section: Section, what: str, detail: str | None = None,
                link: str | None = None) -> None:
        self._add(section, Status.ATENCAO, what, detail, link)

    def falhou(self, section: Section, what: str, detail: str | None = None) -> None:
        self._add(section, Status.FALHOU, what, detail)

    def pulado(self, section: Section, what: str, detail: str | None = None) -> None:
        self._add(section, Status.PULADO, what, detail)

    # ---------- counting ----------

    @property
    def _all(self) -> list[Entry]:
        return [e for s in self.sections for e in s.entries]

    def counts(self) -> dict[Status, int]:
        counts = {s: 0 for s in Status}
        for entry in self._all:
            counts[entry.status] += 1
        return counts

    def needs_you(self) -> list[tuple[Section, Entry]]:
        """Everything still owing a human, paired with where it came from.

        The section travels with the entry because the closing block is read
        out of context: "1 mensagem aguardando resposta" is ambiguous when two
        accounts each have one.
        """
        return [(s, e) for s in self.sections for e in s.entries
                if e.status in (Status.ATENCAO, Status.FALHOU)]

    # ---------- rendering ----------

    def _date_line(self) -> str:
        d = self.when
        return f"{DIAS[d.weekday()]}, {d.day} de {MESES[d.month - 1]} de {d.year}"

    def _summary(self) -> str:
        c = self.counts()
        parts = []
        if c[Status.FEITO]:
            parts.append(f"{c[Status.FEITO]} {'tarefa concluída' if c[Status.FEITO] == 1 else 'tarefas concluídas'}")
        if c[Status.ATENCAO]:
            parts.append(f"{c[Status.ATENCAO]} {'requer' if c[Status.ATENCAO] == 1 else 'requerem'} sua atenção")
        if c[Status.FALHOU]:
            parts.append(f"{c[Status.FALHOU]} não {'foi possível' if c[Status.FALHOU] == 1 else 'foram possíveis'}")
        if not parts:
            return "Nada a relatar."
        return ", ".join(parts) + "."

    def render(self, width: int = 72) -> str:
        rule = "─" * width
        out = [self.titulo.upper(), self._date_line(), rule, "", self._summary()]

        for section in self.sections:
            if not section.entries:
                continue
            out += ["", section.title.upper(), ""]
            for entry in section.entries:
                out.append(f"  {entry.status.value} {entry.what}")
                if entry.detail:
                    for line in entry.detail.splitlines():
                        out.append(f"      {line}")
                if entry.link:
                    out.append(f"      {entry.link}")

        pending = self.needs_you()
        if pending:
            out += ["", rule, "", "PRECISAM DE VOCÊ", ""]
            for section, entry in pending:
                out.append(f"  • {section.title} — {entry.what}")
                if entry.detail:
                    out.append(f"    {entry.detail.splitlines()[0]}")

        out += ["", rule, f"Gerado automaticamente às {self.when:%H:%M}."]
        return "\n".join(out)

    def __str__(self) -> str:
        return self.render()
