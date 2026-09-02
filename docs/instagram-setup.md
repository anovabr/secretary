# Connecting the two Instagram accounts

One Meta app serves both `anova.autismo` and `pankeka.app`. Each account
authorises separately and ends up with its own long-lived token.

Both accounts must be Business or Creator. They are.

## 1. Create the Meta app

At [developers.facebook.com](https://developers.facebook.com/apps) create a new
app, then add the **Instagram** product and choose the setup path for
*Instagram API with Instagram login* (not the Facebook Login variant — that one
needs each account tied to a Facebook Page).

Note the app ID and app secret, then register a redirect URI. It must be https
and match byte for byte what you pass later — but **nothing has to be listening
there.** The browser lands on it with `?code=...` in the address bar and you
copy the code out; whether the page loads or 404s is irrelevant.

So you do not need a domain for the VPS yet. Use a page you already own on
https:

```
https://anovabr.github.io/dashboard/
```

That is registered once and reused for both accounts.

### Add the publishing permission by hand

The use-case setup adds three permissions on its own:

```
instagram_business_basic
instagram_business_manage_comments
instagram_business_manage_messages
```

`instagram_business_content_publish` is **not** among them and must be added
from the *Permissões e recursos* page. Without it everything except publishing
works, so the gap only shows up at the moment you try to post.

### Which app ID

That page shows an **Instagram app ID** and **Instagram app secret**, distinct
from the Meta app's own pair on the main dashboard. The OAuth flow here uses
the Instagram pair. The Meta pair fails with an error that does not explain
itself.

## 2. Add both accounts as testers

While the app is in development mode, only accounts with a role on it can
authorise. In the app dashboard under app roles, add `anova.autismo` and
`pankeka.app` as Instagram testers.

Then accept each invitation **from inside each account**: Instagram app →
Settings → Apps and websites → Tester invites.

This is the step that catches people out. Until the invite is accepted, the
authorise flow fails with a permissions error that does not say why.

Steps 3 and 5 of Meta's checklist do not apply to us:

- **Webhooks** require a published app. We poll hourly instead, which stays
  inside Instagram's 24-hour reply window, so there is nothing to configure.
- **App review** is for reaching accounts that are not yours. Both accounts
  are yours and are testers on the app, so development mode is enough.

## 3. Get a token for each account

If the setup page offers *Gerar token de acesso* next to a connected account,
use it — it returns a long-lived token directly and the rest of this section
is unnecessary. The OAuth flow below is the fallback.

```bash
export IG_APP_ID=... IG_APP_SECRET=... IG_REDIRECT_URI=https://your-vps.example.com/callback

python -m secretary.authorize --url
```

Open that URL in a browser logged in as the first account and approve. You land
on your redirect URI with `?code=...` in the address bar. Copy the code and:

```bash
python -m secretary.authorize --code AQBx... --handle anova.autismo
```

It prints the two lines to paste into `.env`. Repeat for `pankeka.app`, logged
in as that account.

## 4. Turn on message access

Reading and replying to direct messages needs one switch that lives in the
Instagram app, not in the developer dashboard. In **each** account:

> Settings → Messages and story replies → Connected tools →
> **Allow access to messages**

Without it the publishing and comment endpoints work fine and the DM endpoints
return an empty inbox — which looks like "no messages" rather than an error.
If `messages` reports an empty inbox on an account you know has unread DMs,
this switch is why.

## 5. Verify

```bash
python -m secretary.cli whoami
```

Both accounts should report `MEDIA_CREATOR` or `BUSINESS` with a follower count.
Then check the two inboxes:

```bash
python -m secretary.cli inbox      # comentários
python -m secretary.cli messages   # mensagens diretas
```

Nothing above writes anything. The first write should be a `--dry-run`.

## Keeping the tokens alive

Tokens last 60 days and can be renewed any time after they are 24 hours old.
If one lapses, the whole browser flow has to be repeated by hand — so renew on
a schedule, not on expiry:

```bash
python -m secretary.cli refresh-tokens
```

Run it monthly. It prints new values; update `.env` and restart the service.

## Limits worth knowing

| | |
| :-- | :-- |
| Publishing | 50 posts per account per 24 hours |
| Carousels | 2–10 items |
| Media source | public https URL — Instagram fetches it; no file upload |
| DM replies | only within 24 hours of the person's last message |
| Comment replies | no time limit |

## Going beyond your own accounts

Everything above works in development mode because you own both accounts. You
would only need App Review and Advanced Access to act on accounts belonging to
someone else — not the case here.
