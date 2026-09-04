#!/usr/bin/env python3
"""Put the board's Recurring sidebar in the format the secretary reads.

Idempotent: run it again and it changes nothing. Existing tasks keep their
ids (the page merges by id), new ones are added; nothing is deleted.

    set -a; . ./.env; set +a
    python3 tools/board-setup.py            # show what would change
    python3 tools/board-setup.py --write    # write it to the board
"""

import random
import string
import sys
import time
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from secretary.channels import dashboard  # noqa: E402

R = dashboard.ROBOT

# (existing id or None, section, project, text, running order)
WANT = [
    ("ow-insta",      "anova",  "ANOVA/anova autismo", f"{R} Publicar @anova.autismo", 1),
    (None,            "anova",  "ANOVA/anova autismo", f"{R} Responder @anova.autismo", 2),
    ("jmtkhppfhpb2b", "anova",  "ANOVA/anova autismo", f"{R} Painel https://autismo.anovasaude.org/admin.html", 3),
    ("jmtkhn5hw1f9i", "anova",  "ANOVA/anova saude",   f"{R} Painel https://anovasaude.org/admin", 4),
    (None,            "others", None,                  f"{R} Publicar @pankeka.app", 5),
    (None,            "others", None,                  f"{R} Responder @pankeka.app", 6),
    (None,            "anova",  "ANOVA/anova saude",   f"{R} E-mail contato@anovasaude.org", 7),
]


def uid() -> str:
    return "j" + format(int(time.time() * 1000), "x")[:9] + "".join(random.choices(string.ascii_lowercase + string.digits, k=4))


def plan(state: dict) -> list[str]:
    """Apply WANT to the state in place; return one line per change."""
    by_id = {t["id"]: t for t in state["tasks"]}
    by_text = {t.get("text"): t for t in state["tasks"] if t.get("repeat") and t.get("status") not in ("gone", "archived")}
    now = dashboard.now_iso()
    lines = []
    for tid, sec, proj, text, ord_ in WANT:
        t = by_id.get(tid) if tid else by_text.get(text)
        if t is None:
            t = {"id": uid(), "sec": sec, "proj": proj, "text": text, "status": "planning",
                 "date": {"kind": "none", "label": ""}, "addedAt": now, "updatedAt": now,
                 "repeat": "daily", "week": False, "today": False, "tomorrow": False, "month": False, "ord": ord_}
            state["tasks"].append(t)
            lines.append(f"add     {text!r}")
            continue
        want = {"text": text, "sec": sec, "proj": proj, "ord": ord_, "repeat": "daily"}
        diff = {k: v for k, v in want.items() if t.get(k) != v}
        if diff:
            before = t.get("text")
            t.update(diff); t["updatedAt"] = now
            lines.append(f"change  {before!r} -> {text!r}  ({', '.join(diff)})")
        else:
            lines.append(f"keep    {text!r}")
    return lines


def main() -> int:
    write = "--write" in sys.argv
    if write:
        changes = []
        dashboard.update_board(lambda s: changes.extend(plan(s)),
                               message="secretary: recurring tasks in the format the secretary reads")
    else:
        changes = plan(dashboard.load_board())
    print("\n".join(changes))
    print("\n--- Recurring on the board", "after write" if write else "(unchanged; add --write)", "---")
    state = dashboard.load_board() if write else None
    if state:
        for r in dashboard.recurring(state, date.today()):
            print(f"{'✓' if r.done_today else '·'} {r.ord:>2} [{r.section}] {r.text}  ({r.rule})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
