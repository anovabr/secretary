# Reading the anovasaude panels

Three of the eight daily steps read your own admin pages:

- `autismo.anovasaude.org/admin.html` — new assessments, new registrations
- anovasaude admin — assessments performed
- anovasaude admin — professionals registered

There are two ways to do this, and they are not close in quality.

## The good way: a read-only endpoint

Because you own the system, the panel is drawing its numbers from somewhere.
Expose that same data as JSON behind a token the agent holds:

```
GET /api/admin/summary?since=2026-09-02
Authorization: Bearer <token issued for the secretary>

{
  "assessments": {"new": 7, "completed": 5, "in_progress": 2,
                  "abandoned_at_step": {"3": 2}},
  "registrations": {"guardians": 4},
  "professionals": [{"id": 91, "name": "...", "council_number": null}]
}
```

This is a few hours of work on your side and it removes the whole fragile
category: no login flow, no 2FA, no session expiry, no breakage when you
restyle the panel, no screen-scraping heuristics that silently start
returning zero. The agent asks a question and gets an answer.

It is also safer. A read-only, scoped token can see counts and pending
registrations and nothing else. A browser session logged into the admin can
do anything an administrator can do.

## The fallback: browser automation

If exposing an endpoint is not practical, Playwright drives a real browser
with a persistent profile so the login survives between runs. This works, and
it is what the VPS is for — but expect it to need repair whenever the panel
changes, and it needs a stored admin session, which is a much broader
credential than the token above.

## Recommendation

Do the endpoint. It is the difference between a step that quietly works for
a year and one you keep fixing. If you tell me what the panel queries, I can
write the endpoint for whatever stack `anovasaude.org` runs on.
