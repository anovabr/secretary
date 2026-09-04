# secretary

A daily agent for two Instagram accounts: it publishes the day's carousel,
answers ordinary messages, reports everything else, and leaves the judgement
calls to a person.

Runs on a VPS from cron. Nothing here reaches Instagram without a token, and
the token is never in this repository.

## Accounts

| | |
| :--- | :--- |
| `anova.autismo` | Autism screening — [autismo.anovasaude.org](https://autismo.anovasaude.org) |
| `pankeka.app` | The Pankeka app |

## Where things are

```
secretary/       the program — see secretary/README.md
media/           the slides and captions, one folder per post
tools/           the slide generator, and the cron wrapper
docs/            Meta setup, and the admin-panel question
routine.md       what runs, in what order
```

## Running it

```bash
cp .env.example .env      # add the tokens; chmod 600; never committed
pip install -r requirements.txt

python -m secretary.cli whoami         # check the tokens
./tools/run-secretary.sh --dry-run     # the whole routine, writing nothing
```

Then install the schedule in `tools/crontab.example`.

## Two things that must stay true

**The media stays public.** Instagram fetches images from a URL — there is no
upload — so `media/` has to be readable without credentials. If this repository
ever goes private, move the images somewhere public and set `IG_MEDIA_BASE` to
point there; nothing else changes.

**The reports stay private.** `reports/` quotes real messages from real people
writing to an autism screening account. It is gitignored and belongs only on
the machine that produced it.

## Earlier work

| When | What | Where it went |
| :--- | :--- | :--- |
| Jul 2026 | One-page site for [@paws.vica](https://www.instagram.com/paws.vica) | [anovabr/vica](https://github.com/anovabr/vica) · [live](https://anovabr.github.io/vica/) |

This repository began as a scratch sandbox; that history is still in the log.
