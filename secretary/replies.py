"""Standard replies, and the judgement about when not to send one.

An account about autism screening receives messages from people in real
distress. A canned reply to someone in crisis is worse than no reply, so the
rule here is narrow: send the standard acknowledgement to ordinary enquiries,
and hand anything else to a human untouched.

The reply never answers the question. It confirms the message arrived and
points at the screening — anything requiring a real answer stays in the report.
"""

from __future__ import annotations

import re

# Sent once per conversation, to first-time enquiries only.
STANDARD_REPLY = {
    "anova.autismo": (
        "Olá! Obrigado pela mensagem.\n\n"
        "O rastreio gratuito está no link do perfil — leva cerca de 8 minutos, "
        "não exige cadastro e o resultado sai na hora.\n\n"
        "Importante: o rastreio indica se vale investigar, mas não é "
        "diagnóstico. Para isso é necessária uma avaliação com profissional "
        "habilitado."
    ),
    "pankeka.app": (
        "Olá! Obrigado pela mensagem.\n\n"
        "Vamos verificar e retornamos em breve."
    ),
}

# Anything here goes to a person, never to a template. Deliberately broad:
# a false positive costs one manual reply, a false negative costs much more.
_ESCALATE = re.compile(
    r"suic[ií]d|me matar|tirar (a )?minha vida|n[ãa]o quero (mais )?viver|"
    r"automutil|me cortar|me machucar|"
    r"desespero|surto|crise|emerg[êe]ncia|socorro|urgente|"
    r"processo|advogad|reclama[çc][ãa]o|procon|denunci|"
    r"reembolso|estorno|cobran[çc]a|n[ãa]o recebi",
    re.IGNORECASE,
)


def needs_a_person(text: str) -> bool:
    """True when this message must not receive a standard reply."""
    return bool(_ESCALATE.search(text or ""))


def standard_reply(handle: str) -> str | None:
    return STANDARD_REPLY.get(handle)
