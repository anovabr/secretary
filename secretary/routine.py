"""Assembles the routine's steps in the order the board lists them.

Only steps that can be done properly are here. The panels and the mailbox are
absent rather than stubbed — a step that pretends to run is worse than one
that is visibly missing.

Replies are not sent automatically yet. Until the standard answers exist, the
message and comment steps triage and report: you see who is waiting and what
they asked, and the reply stays yours. Turning that into an auto-reply is a
change in one place once the texts are agreed.
"""

from __future__ import annotations

from datetime import date

from .accounts import load_accounts
from .channels.instagram import Instagram
from .media import Post, post_for
from .runner import Step, StepContext


def _plural(n: int, one: str, many: str) -> str:
    return f"{n} {one if n == 1 else many}"


def instagram_messages(handle: str) -> Step:
    """Report the direct messages waiting on a reply."""

    def run(ctx: StepContext) -> None:
        ig = Instagram(load_accounts()[handle], dry_run=ctx.dry_run)
        pending = ig.unanswered_threads()
        if not pending:
            ctx.feito("Caixa de entrada vazia")
            return

        answerable = [t for t in pending if t["within_window"]]
        stale = [t for t in pending if not t["within_window"]]

        if answerable:
            detail = "\n".join(f"@{t['sender']}: {t['text'].strip()[:90]}" for t in answerable[:6])
            ctx.atencao(_plural(len(answerable), "mensagem aguardando resposta",
                                "mensagens aguardando resposta"), detail)
        if stale:
            detail = "\n".join(
                f"@{t['sender']}, há {int(t['age'].total_seconds() // 3600)}h: {t['text'].strip()[:80]}"
                for t in stale[:6]
            )
            ctx.atencao(_plural(len(stale), "mensagem fora da janela de 24 horas",
                                "mensagens fora da janela de 24 horas"),
                        detail + "\nSó podem ser respondidas manualmente pelo aplicativo.")

    return Step(key=f"messages:{handle}", title=f"Instagram · {handle}", run=run, once_per_day=False)


def instagram_comments(handle: str) -> Step:
    """Report comments nobody has answered."""

    def run(ctx: StepContext) -> None:
        ig = Instagram(load_accounts()[handle], dry_run=ctx.dry_run)
        pending = list(ig.unanswered_comments())
        if not pending:
            ctx.feito("Nenhum comentário pendente")
            return
        detail = "\n".join(f"@{c.get('username', '?')}: {c.get('text', '').strip()[:90]}"
                           for c in pending[:6])
        ctx.atencao(_plural(len(pending), "comentário sem resposta", "comentários sem resposta"),
                    detail)

    return Step(key=f"comments:{handle}", title=f"Instagram · {handle}", run=run, once_per_day=False)


def instagram_post(handle: str, post: Post) -> Step:
    """Publish the day's post — carousel or single image, as the folder holds."""

    def run(ctx: StepContext) -> None:
        ig = Instagram(load_accounts()[handle], dry_run=ctx.dry_run)
        if post.is_carousel:
            media_id = ig.publish_carousel(post.image_urls, post.caption)
            kind = f"Carrossel, {len(post.image_urls)} imagens"
        else:
            media_id = ig.publish_image(post.image_urls[0], post.caption)
            kind = "Imagem única"
        first_line = post.caption.splitlines()[0] if post.caption else "(sem legenda)"
        ctx.feito("Publicação realizada",
                  f'{kind} — "{first_line[:70]}"\npasta: {post.name}',
                  f"media id {media_id}")

    return Step(key=f"post:{handle}", title=f"Instagram · {handle}", run=run)


def daily(today: date | None = None, root: str = "media") -> list[Step]:
    """The morning run.

    The day's post for each account comes from media/<handle>/, one folder a
    day in order. An account with no folders prepared simply has no publishing
    step — its messages and comments are still handled.
    """
    steps: list[Step] = []

    for handle in ("anova.autismo", "pankeka.app"):
        post = post_for(handle, today=today, root=root)
        if post:
            steps.append(instagram_post(handle, post))
        steps.append(instagram_messages(handle))
        steps.append(instagram_comments(handle))

    return steps


def hourly() -> list[Step]:
    """The hourly check: messages and comments on both accounts, nothing else."""
    steps: list[Step] = []
    for handle in ("anova.autismo", "pankeka.app"):
        steps += [instagram_messages(handle), instagram_comments(handle)]
    return steps
