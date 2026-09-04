# Secretary

A daily agent that works through a list: publishing posts, answering comments,
handling mail, checking submissions.

This directory is scaffolding. It is meant to move to a **private** repo before
any real token exists — this one is a public sandbox and must never hold
credentials.

## What works today

Instagram, for `anova.autismo` and `pankeka.app`: publish images, carousels and
reels; find comments and direct messages nobody has answered; reply to both;
renew tokens. Plus the daily report the run hands back.

The routine itself is in [../routine.md](../routine.md).

See [../docs/instagram-setup.md](../docs/instagram-setup.md) to get the tokens,
then:

```bash
pip install -r requirements.txt
cp .env.example .env       # fill it in
set -a; source .env; set +a

python -m secretary.cli whoami
python -m secretary.cli inbox        # comentários sem resposta
python -m secretary.cli messages     # mensagens diretas sem resposta
python -m secretary.cli report       # exemplo do relatório diário
python -m secretary.cli board        # as rotinas de hoje no quadro, e de quem são
python -m secretary.cli run --dry-run    # a rotina inteira, sem escrever nada
python -m secretary.cli run --hourly     # só a verificação de hora em hora
python -m secretary.cli post --account pankeka.app --image https://... --caption "..." --dry-run
```

`--dry-run` prints every write instead of sending it. Keep using it until you
trust a given account.

## Tests

```bash
python -m unittest discover -s secretary -p "test_*.py" -t .
```

88 tests, no network — the transport is stubbed throughout. They cover the
comment and DM filters, the 24-hour reply window, carousel limits, report
formatting, and the runner's three promises: a failed step doesn't stop the
run, nothing publishes twice in a day, and a dry run leaves no trace.

## Layout

```
secretary/
  channels/instagram.py   API client: publish, comments, direct messages
  channels/dashboard.py   the task board: decrypts taskboard.json, parses 🤖 tasks, ticks them
  accounts.py             multi-account config from the environment
  authorize.py            one-time OAuth code -> long-lived token
  cli.py                  command line
  report.py               the daily report
  demo_report.py          a worked example of it
  runner.py               executes steps, isolates failures, prevents repeats
  routine.py              builds the morning run from the board's Recurring sidebar
  media.py                picks the day's post from media/<handle>/
  replies.py              the standard reply, and when not to send it
  test_instagram.py       tests
  test_runner.py          tests
  test_dashboard.py       tests
```

Other channels become siblings of `channels/instagram.py`. Next are the
anovasaude panels (see [../docs/paineis.md](../docs/paineis.md)) and the
`contato@anovasaude.org` mailbox — both unblocked.

TikTok and WhatsApp are not part of the routine and are not being built.
