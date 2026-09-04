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
python3 -m unittest discover -s secretary -p "test_*.py" -t .   # 69 tests, no network
python3 -m secretary.cli whoami                                  # check both tokens
./tools/run-secretary.sh --dry-run                               # whole routine, writes nothing
```

Tokens last 60 days. `python3 -m secretary.cli refresh-tokens` prints new ones
to paste into `.env`; run it monthly, well before expiry. Once a token lapses
the whole browser flow has to be redone by hand.

## How it works

`runner.py` executes steps in order and makes three promises the tests hold it
to: a failed step never stops the run, nothing publishes twice in a day, and a
dry run leaves no trace. `routine.py` assembles the steps, `media.py` picks the
day's folder (one per day, cycling), `report.py` builds the Portuguese report.

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

## State

Working: both accounts authenticated, 20 carousels prepared for
`anova.autismo` with captions, auto-reply, the daily report.

Open, roughly in the order the owner wants them:

- **More carousels for `anova.autismo`** — twenty exist. Next ask is about
  ten more, researched from current literature, same citation discipline
- **`pankeka.app` has no posts.** `media/pankeka.app/` is empty, and nobody
  has yet said what the app does or who it is for — ask before writing
- Its standard DM reply is a placeholder written without knowing the product
- The 20 captions are a first draft and want a human read
- Report delivery: currently `reports/<date>.txt` plus whatever cron mails
- **The anovasaude admin panels** — three of the four tasks on the owner's
  board, and the largest remaining piece. See `docs/paineis.md`: a read-only
  JSON endpoint beats browser automation by a wide margin, and the choice is
  the owner's to make
- **`contato@anovasaude.org` triage** — not built; the mail provider is still
  unknown, which decides between an API and plain IMAP
- **Report delivery by email** — wanted, not built. Currently a file in
  `reports/` plus whatever cron mails locally. Needs an SMTP account
- **The other sites on this VPS** — not yet looked at; ask what they are
