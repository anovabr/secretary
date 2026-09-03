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

## 2. Verify the business first

An app owned by a Meta business portfolio cannot connect an Instagram account
until that business is confirmed. Until it is, *Adicionar conta* fails with
**"Insufficient Developer Role"** — which sounds like a permissions problem on
your Facebook user and is not. Confirmation takes about two business days.

Being Administrador on the app does not substitute for it.

## 3. Connect each account

Ignore the **Funções** page. Its Administradores / Desenvolvedores / Testadores
roles are Facebook app roles from the older Basic Display flow, and no Instagram
tester invitation is involved here.

Instead, on the API setup page under *Gerar tokens de acesso*, use **Adicionar
conta**. That opens an Instagram login window; sign in as the account and
approve. Then generate its token.

**Use a private window for each account.** The login window reuses whatever
Instagram session the browser already holds, so the second account silently
reconnects the first unless the session is empty.

Steps 3 and 5 of Meta's checklist do not apply to us:

- **Webhooks** require a published app. We poll hourly instead, which stays
  inside Instagram's 24-hour reply window, so there is nothing to configure.
- **App review** is for reaching accounts that are not yours. Both accounts
  are yours and are testers on the app, so development mode is enough.

## 4. The OAuth fallback

*Adicionar conta* is the normal path and returns a long-lived token directly.
Everything below is only needed if that button is unavailable.

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

## 5. Turn on message access

Reading and replying to direct messages needs one switch that lives in the
Instagram app, not in the developer dashboard. In **each** account:

> Settings → Messages and story replies → Connected tools →
> **Allow access to messages**

Without it the publishing and comment endpoints work fine and the DM endpoints
return an empty inbox — which looks like "no messages" rather than an error.
If `messages` reports an empty inbox on an account you know has unread DMs,
this switch is why.

## 6. Verify

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
