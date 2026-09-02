# Connecting the two Instagram accounts

One Meta app serves both `anova.autismo` and `pankeka.app`. Each account
authorises separately and ends up with its own long-lived token.

Both accounts must be Business or Creator. They are.

## 1. Create the Meta app

At [developers.facebook.com](https://developers.facebook.com/apps) create a new
app, then add the **Instagram** product and choose the setup path for
*Instagram API with Instagram login* (not the Facebook Login variant — that one
needs each account tied to a Facebook Page).

Note the app ID and app secret. Register your redirect URI; it must be https and
match byte for byte what you pass later. If you have a domain pointing at the
VPS, `https://your-vps.example.com/callback` is fine — nothing needs to be
listening there, you are only reading the code out of the address bar.

## 2. Add both accounts as testers

While the app is in development mode, only accounts with a role on it can
authorise. In the app dashboard under app roles, add `anova.autismo` and
`pankeka.app` as Instagram testers.

Then accept each invitation **from inside each account**: Instagram app →
Settings → Apps and websites → Tester invites.

This is the step that catches people out. Until the invite is accepted, the
authorise flow fails with a permissions error that does not say why.

## 3. Get a token for each account

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

## 4. Verify

```bash
python -m secretary.cli whoami
```

Both accounts should report `MEDIA_CREATOR` or `BUSINESS` with a follower count.

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
