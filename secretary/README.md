# Secretary

A daily agent that works through a list: publishing posts, answering comments,
handling mail, checking submissions.

This directory is scaffolding. It is meant to move to a **private** repo before
any real token exists — this one is a public sandbox and must never hold
credentials.

## What works today

Instagram, for `anova.autismo` and `pankeka.app`: publish images, carousels and
reels; find comments nobody has answered; reply to them; renew tokens.

See [../docs/instagram-setup.md](../docs/instagram-setup.md) to get the tokens,
then:

```bash
pip install -r requirements.txt
cp .env.example .env       # fill it in
set -a; source .env; set +a

python -m secretary.cli whoami
python -m secretary.cli inbox
python -m secretary.cli post --account pankeka.app --image https://... --caption "..." --dry-run
```

`--dry-run` prints every write instead of sending it. Keep using it until you
trust a given account.

## Tests

```bash
python -m secretary.test_instagram
```

Nine tests, no network — the transport is stubbed.

## Layout

```
secretary/
  channels/instagram.py   API client: publish, read comments, reply
  accounts.py             multi-account config from the environment
  authorize.py            one-time OAuth code -> long-lived token
  cli.py                  command line
  test_instagram.py       tests
```

Other channels become siblings of `channels/instagram.py`. Email is next and is
unblocked; TikTok and WhatsApp wait on approvals described in the build plan.
