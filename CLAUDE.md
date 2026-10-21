# secretary

A daily agent for two Instagram accounts, running on this VPS from cron.
Published by `tools/run-secretary.sh`; the routine is in `routine.md`.

| Account | What it is |
| :--- | :--- |
| `anova.autismo` | Autism screening — autismo.anovasaude.org |
| `pankeka.app` | The Pankeka app |

## Rules

**Never print, echo, log or commit the contents of `.env`.** It holds two
60-day Instagram tokens. Read them into the environment and nothing else.

**Never commit `reports/`.** It quotes real messages from real people writing
to an autism screening account. Gitignored — keep it that way.

**`media/` must stay publicly readable.** Instagram fetches images by URL;
there is no upload. If this repository ever goes private the images have to
move somewhere public and `IG_MEDIA_BASE` has to point there.

**Always `--dry-run` first.** A live run publishes to a real account with real
followers, and marks the day done so the 07:00 job then skips it.

**Never auto-reply to distress.** `secretary/replies.py` holds a deliberately
broad pattern — self-harm, crisis, urgency, complaints, legal. Those go to the
report for a person. Widen it freely; do not narrow it without being asked.

## Running

```bash
python3 -m unittest discover -s secretary -p "test_*.py" -t .   # 131 tests, no network
python3 -m secretary.cli whoami                                  # check both tokens
./tools/run-secretary.sh --dry-run                               # whole routine, writes nothing
```

Tokens last 60 days. `python3 -m secretary.cli refresh-tokens` prints new ones
to paste into `.env`; run it monthly, well before expiry. Once a token lapses
the whole browser flow has to be redone by hand.

## The board is the routine

anovabr.github.io/dashboard is where the routine is configured; its
**Recurring** sidebar is the list the morning run executes. Change it there,
not in routine.py. A recurring task is the secretary's when its text starts
with 🤖 followed by a verb it knows and a target — `🤖 Publicar @anova.autismo`,
`🤖 Responder @conta`, `🤖 Painel <url>`, `🤖 E-mail <endereço>` — see
routine.md for the table. Tasks without the robot are the owner's and are only
listed. The secretary ticks what it completes (`lastDone`, the page's own
convention) and writes back through the page's own sync: fetch, merge by task
id and `updatedAt`, put with the file's sha. Board state: `taskboard.json` on
the `state` branch of anovabr/dashboard, AES-256-GCM under `DASHBOARD_PASSWORD`
(in `.env` on the VPS; the write token comes from `gh auth`). If the board is
unreachable the built-in list runs instead. `tools/board-setup.py` puts the
sidebar in this format and is idempotent.

**The user will not edit `.env` by hand.** Secrets are pasted in chat and
stored by Claude, never echoed.

## The panels are read from their databases

`🤖 Painel <url>` is served by `channels/panels.py`: one adapter per site,
keyed by URL. Both known panels run on this VPS, so they are read straight
from SQLite (`/opt/anovasaude/admin/anova.db`, `/opt/autismosaude/users.db`)
in read-only mode — no login, nothing to expire. A URL with no adapter is
reported as "não entendi" with the known list. `.secretary-panels.json`
holds per-table watermarks so each morning reports only what is new; dry
runs never advance it. **Those databases hold names and e-mails: tests use
fake databases, never the real files, and the report is the only place
their contents go.** The permission classifier blocks ad-hoc reads of them
from a Claude session; that is fine — cron reads them.

## How it works

`runner.py` executes steps in order and makes three promises the tests hold it
to: a failed step never stops the run, nothing publishes twice in a day, and a
dry run leaves no trace. `routine.py` assembles the steps, `media.py` picks the
day's entry (a queue: new before repeated, a reel after every two carousels, logged in `.secretary-published.json`) and the day's story, `report.py` builds the Portuguese report.

## Things that cost hours to learn

**Two ids, one account.** The id in Meta's dashboard (`17841...`) and the id
the API returns are different identifier spaces. Comparing one against the
other fails silently rather than erroring. The code addresses the account as
`me` and asks the API for its own id — do not reintroduce a configured id.

**Timestamps.** Instagram sends `+0000`; `datetime.fromisoformat` only accepts
a colon-less offset from Python 3.11, and this box runs 3.10. `_age_of`
normalises it. Without that every message reads as ageless and the 24-hour
reply window looks closed.

**Meta's dashboard lies in two places.** The permission list on the API setup
page is static text, identical for every app — only *Permissões e recursos* is
real, where "Pronto para teste" means usable. And "Insufficient Developer Role"
means the owning business is unverified, not that a role is missing.

## Asked for and settled

**Following accounts is not possible and must not be attempted.** The
Instagram API has no follow endpoint — Meta excludes it deliberately to stop
mass-following. The only route is browser automation, which breaks Instagram's
terms and gets accounts action-blocked. If asked to follow accounts, offer a
researched *list* for a person to follow by hand instead.

**Volume: aim for tens of good posts, not thousands.** One post a day means
sixty covers two months. The twenty existing carousels carry thirty-two
scientific references, and that is what makes the account credible rather than
a content mill. If asked for hundreds or thousands, say what the arithmetic
actually is and offer twenty good ones.

**Comments are reported, never answered automatically.** A public reply is
more exposed than a DM. Do not turn on comment auto-reply without being asked
directly.

**Reels are files, not a new pipeline.** A `.mp4` or `.mov` under
`media/<conta>/` publishes as a reel from the same queue — loose,
named as the editor exported it, with an optional `.txt` caption and `.jpg`
cover sharing its name. A folder of images is still a carousel. The files
decide, so adding reels is copying them in — no board change, no new verb, no
second queue. URLs are percent-encoded because the exported names have
spaces in them. Video comes from GitHub like the images; the three reels of
27–29 September proved it works, so `IG_VIDEO_BASE` is only an escape hatch.

**Stories are loose `story-NN-slug.png` files**, one a day with the post. One
ending in a post's slug goes out with that post only; the rest take turns. The
API cannot add a link sticker — buttons drawn into a story do nothing.

**Who makes the slides.** Most material arrives from the owner as finished
folders. Claude checks those (claims, addresses, captions) and never re-renders
or redesigns them. Since 2026-10-21 the owner has also asked Claude to make new
posts. Posts 55–64 and their stories, plus three reels, come from
`tools/slides/` (render.py, reel.py, posts.py), in the three looks in
`docs/formatos.md`. The owner's local folder numbering continues from there.

**`/novo-post`** writes a new carousel in the house style — five slides, a
reference on every factual claim, matching caption. Use it rather than
inventing a format.

## The goal

Every day: one or two carousels on `anova.autismo`, one post on
`pankeka.app`, replies on both, and one report covering both accounts. Then
the other sites hosted on this VPS.

**The content arithmetic is the binding constraint.** Two carousels a day
consumes the twenty prepared posts in ten days; with pankeka that is roughly
ninety posts a month. Writing at that rate is what turns an account with
thirty-two citations into a content mill, and the citations are the whole
reason this one is worth following.

So: publish one a day until a real backlog exists, and treat "two a day" as
something to earn rather than a default. When asked for more posts, research
properly and write few — never pad.

**Nothing about other accounts.** With Instagram Login there is no way to
look up, search for, or follow another account. Business Discovery (the only
lookup Meta offers) is Facebook-Login-only and needs `instagram_basic`,
`instagram_manage_insights` and a Page — with these tokens every version of
the API answers "Tried accessing nonexisting field (business_discovery)".
Following has no API at all; automating it means unofficial clients, which
get accounts suspended. Following is done by hand, from the app. Verified
2026-09-03; a `lookup` command was built and reverted.

## State

Working: both accounts authenticated, 30 carousels prepared and rendered for
`anova.autismo` with captions (approved by the owner 2026-10-15), auto-reply, the daily report. Posts 36–54 (by
the owner), two more reels and three stories joined the queue on 2026-10-09;
reels and stories publish from GitHub. Posts 55–64, their ten stories and
three reels (made by Claude, `tools/slides/`) joined on 2026-10-21. The queue
then runs to about 20 November.

Open, roughly in the order the owner wants them:

- **post-35 waits in `entrada/`**: slides 2 and 4 still hold the editor's
  empty photo boxes ("Solte uma foto aqui"). Move it into `media/` once fixed
- `video_prevalencia.mp4` was in the owner's folder but never uploaded
- **`pankeka.app` has no posts.** `media/pankeka.app/` is empty, and nobody
  has yet said what the app does or who it is for — ask before writing
- Its standard DM reply is a placeholder written without knowing the product
- Report delivery: `reports/<date>.txt`; the 07:00 run e-mails it via `secretary/deliver.py` once SMTP_PASSWORD (Titan, contato@anovasaude.org) is in .env
- **The anovasaude admin panels** — three of the four tasks on the owner's
  board, and the largest remaining piece. See `docs/paineis.md`: a read-only
  JSON endpoint beats browser automation by a wide margin, and the choice is
  the owner's to make
- **`contato@anovasaude.org` triage** — not built; the mail provider is still
  unknown, which decides between an API and plain IMAP
- **Report delivery by email** — wanted, not built. Currently a file in
  `reports/` plus whatever cron mails locally. Needs an SMTP account
- **The other sites on this VPS** — not yet looked at; ask what they are
