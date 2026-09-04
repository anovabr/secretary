"""Assembles the routine's steps in the order the board lists them.

The morning run is built from the task board's Recurring sidebar
(channels/dashboard.py): every recurring task due today that starts with 🤖
becomes a step here, in board order, and is ticked on the board when it
succeeds. Tasks without the robot are the owner's and are only listed. If
the board cannot be read the built-in list runs instead, so a GitHub outage
never costs a post.

The panels and the mailbox are not built; a board task asking for them is
reported as such rather than pretended.

Replies are not sent automatically yet. Until the standard answers exist, the
message and comment steps triage and report: you see who is waiting and what
they asked, and the reply stays yours. Turning that into an auto-reply is a
change in one place once the texts are agreed.
"""

from __future__ import annotations

from datetime import date

from .accounts import load_accounts
from .channels import dashboard
from .channels.instagram import Instagram
from .media import Post, post_for
from .replies import needs_a_person, standard_reply
from .runner import Step, StepContext


def _plural(n: int, one: str, many: str) -> str:
    return f"{n} {one if n == 1 else many}"


def instagram_messages(handle: str) -> Step:
    """Reply to ordinary enquiries; leave anything else for a person."""

    def run(ctx: StepContext) -> None:
        ig = Instagram(load_accounts()[handle], dry_run=ctx.dry_run)
        pending = ig.unanswered_threads()
        if not pending:
            ctx.feito("Caixa de entrada vazia")
            return

        answerable = [t for t in pending if t["within_window"]]
        stale = [t for t in pending if not t["within_window"]]

        reply = standard_reply(handle)
        sent, escalated, failed = [], [], []
        for thread in answerable:
            if not reply or needs_a_person(thread["text"]):
                escalated.append(thread)
                continue
            try:
                ig.send_message(thread["sender_id"], reply)
                sent.append(thread)
            except Exception as exc:                      # noqa: BLE001 — one
                failed.append((thread, exc))              # bad thread must not
                                                          # stop the others
        if sent:
            ctx.feito(_plural(len(sent), "mensagem respondida", "mensagens respondidas"),
                      "\n".join(f"@{t['sender']}: {t['text'].strip()[:80]}" for t in sent[:6]))
        if escalated:
            ctx.atencao(_plural(len(escalated), "mensagem para você responder",
                                "mensagens para você responder"),
                        "\n".join(f"@{t['sender']}: {t['text'].strip()[:90]}" for t in escalated[:6])
                        + "\nNão foram respondidas automaticamente.")
        if failed:
            ctx.atencao(_plural(len(failed), "mensagem falhou ao enviar",
                                "mensagens falharam ao enviar"),
                        "\n".join(f"@{t['sender']}: {exc}" for t, exc in failed[:4]))
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


def board_summary(due: list[dashboard.Routine]) -> Step:
    """What the board says recurs today, robot and human alike, and what is ticked."""

    def run(ctx: StepContext) -> None:
        if not due:
            ctx.feito("Nenhuma rotina prevista para hoje no quadro")
            return
        lines = [f"{'✓' if r.done_today else '·'} {'🤖 ' if r.mine else ''}[{r.section}] {r.label}  ({r.rule})"
                 for r in due]
        ctx.feito(_plural(len(due), "rotina prevista para hoje", "rotinas previstas para hoje"),
                  "\n".join(lines))
        yours = [r for r in due if not r.mine and not r.done_today]
        if yours:
            ctx.atencao(_plural(len(yours), "rotina sua ainda não marcada no quadro",
                                "rotinas suas ainda não marcadas no quadro"),
                        "\n".join(f"[{r.section}] {r.label}" for r in yours))

    return Step(key="board:summary", title="Quadro · rotinas de hoje", run=run, once_per_day=False)


def board_unavailable(exc: Exception) -> Step:
    def run(ctx: StepContext) -> None:
        ctx.atencao("Quadro não lido — usando a lista embutida", str(exc))

    return Step(key="board:unavailable", title="Quadro · rotinas de hoje", run=run, once_per_day=False)


def board_not_configured() -> Step:
    def run(ctx: StepContext) -> None:
        ctx.atencao("Nenhuma rotina do quadro é da secretária — usando a lista embutida",
                    "Marque as tarefas dela com 🤖 (veja routine.md), ou rode tools/board-setup.py.")

    return Step(key="board:not-configured", title="Quadro · rotinas de hoje", run=run, once_per_day=False)


def not_understood(routine: dashboard.Routine) -> Step:
    def run(ctx: StepContext) -> None:
        ctx.atencao("Não entendi esta rotina do quadro",
                    f"{routine.text}\nFormato: 🤖 Publicar @conta · Responder @conta · Painel <url> · E-mail <endereço>")

    return Step(key=f"board:{routine.id}", title="Quadro · rotinas de hoje", run=run, once_per_day=False)


def not_built(routine: dashboard.Routine, what: str) -> Step:
    def run(ctx: StepContext) -> None:
        ctx.atencao(f"{what} ainda não existe", f"{routine.label}\nFica no quadro sem marcar até existir.")

    return Step(key=f"board:{routine.id}", title="Quadro · rotinas de hoje", run=run, once_per_day=False)


def no_post(handle: str) -> Step:
    def run(ctx: StepContext) -> None:
        ctx.atencao("Sem post preparado", f"media/{handle}/ não tem pastas com imagens.")

    return Step(key=f"post:{handle}", title=f"Instagram · {handle}", run=run, once_per_day=False)


def _ticking(step: Step, routine_id: str, ticks: list[str], parts: list[int]) -> Step:
    """Wrap a step so the routine is ticked once all its parts succeeded."""
    inner = step.run

    def run(ctx: StepContext) -> None:
        inner(ctx)
        parts[0] -= 1
        if parts[0] <= 0 and routine_id not in ticks:
            ticks.append(routine_id)

    return Step(key=step.key, title=step.title, run=run, once_per_day=step.once_per_day)


def board_tick(ticks: list[str]) -> Step:
    """Last step: mark on the board what the run completed."""

    def run(ctx: StepContext) -> None:
        if not ticks:
            return
        if ctx.dry_run:
            print(f"  [dry-run] tick on board: {ticks}")
        else:
            dashboard.tick(ticks)
        ctx.feito(_plural(len(ticks), "rotina marcada no quadro", "rotinas marcadas no quadro"))

    return Step(key="board:tick", title="Quadro · rotinas de hoje", run=run, once_per_day=False)


def steps_for(routine: dashboard.Routine, ticks: list[str], today: date, root: str) -> list[Step]:
    """The steps one robot task asks for."""
    cmd = routine.command
    if cmd is None:
        return [not_understood(routine)]
    if cmd.action == "publish":
        handle = cmd.target
        post = post_for(handle, today=today, root=root)
        if post is None:
            return [no_post(handle)]
        return [_ticking(instagram_post(handle, post), routine.id, ticks, [1])]
    if cmd.action == "reply":
        handle = cmd.target
        parts = [2]
        return [_ticking(instagram_messages(handle), routine.id, ticks, parts),
                _ticking(instagram_comments(handle), routine.id, ticks, parts)]
    if cmd.action == "panel":
        return [not_built(routine, "O leitor de painéis")]
    if cmd.action == "mail":
        return [not_built(routine, "A triagem de e-mail")]
    return [not_understood(routine)]


def from_board(state: dict, today: date | None = None, root: str = "media") -> list[Step]:
    """The morning run as the board describes it."""
    today = today or date.today()
    routines = dashboard.recurring(state, today)
    due = [r for r in routines if r.due_today]
    if not any(r.mine for r in routines):
        # Nothing on the board is addressed to the secretary yet: the board
        # is not configured for it, and silence would cost the day's post.
        return [board_summary(due), board_not_configured()] + builtin_daily(today, root)
    ticks: list[str] = []
    steps = [board_summary(due)]
    for r in due:
        if r.mine and not r.done_today:
            steps += steps_for(r, ticks, today, root)
    steps.append(board_tick(ticks))
    return steps


def builtin_daily(today: date | None = None, root: str = "media") -> list[Step]:
    """The fallback when the board cannot be read: both accounts, post then reply."""
    steps: list[Step] = []
    for handle in ("anova.autismo", "pankeka.app"):
        post = post_for(handle, today=today, root=root)
        if post:
            steps.append(instagram_post(handle, post))
        steps.append(instagram_messages(handle))
        steps.append(instagram_comments(handle))
    return steps


def daily(today: date | None = None, root: str = "media") -> list[Step]:
    """The morning run: the board's list, or the built-in one if the board is unreachable."""
    try:
        state = dashboard.load_board()
    except dashboard.DashboardError as exc:
        return [board_unavailable(exc)] + builtin_daily(today, root)
    return from_board(state, today, root)


def hourly() -> list[Step]:
    """The hourly check: messages and comments on both accounts, nothing else."""
    steps: list[Step] = []
    for handle in ("anova.autismo", "pankeka.app"):
        steps += [instagram_messages(handle), instagram_comments(handle)]
    return steps
