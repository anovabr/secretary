"""One-time helper: turn an OAuth code into a long-lived Instagram token.

Run this once per account. The flow is:

  1. Open the authorise URL this script prints, logged in as the account you
     want to connect. Approve the permissions.
  2. Instagram redirects to your redirect URI with ?code=... in the address bar.
     Copy that code (everything up to, but not including, any "#_" suffix).
  3. Feed it back here. You get a token valid ~60 days and the account's user id.

    python -m secretary.authorize --url
    python -m secretary.authorize --code AQBx...

IG_APP_ID, IG_APP_SECRET and IG_REDIRECT_URI must be set. The redirect URI has
to match what is registered in the app dashboard exactly, https, no fragment.
"""

from __future__ import annotations

import argparse
import os
import sys
from urllib.parse import urlencode

import requests

SCOPES = [
    "instagram_business_basic",
    "instagram_business_content_publish",
    "instagram_business_manage_comments",
    "instagram_business_manage_messages",
]


def _env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"error: {name} is not set")
    return value


def authorize_url() -> str:
    query = urlencode({
        "client_id": _env("IG_APP_ID"),
        "redirect_uri": _env("IG_REDIRECT_URI"),
        "response_type": "code",
        "scope": ",".join(SCOPES),
    })
    return f"https://www.instagram.com/oauth/authorize?{query}"


def exchange(code: str) -> dict:
    """Swap the one-time code for a short-lived token, then a long-lived one."""
    code = code.split("#")[0]  # Instagram appends "#_" to the redirect

    short = requests.post(
        "https://api.instagram.com/oauth/access_token",
        data={
            "client_id": _env("IG_APP_ID"),
            "client_secret": _env("IG_APP_SECRET"),
            "grant_type": "authorization_code",
            "redirect_uri": _env("IG_REDIRECT_URI"),
            "code": code,
        },
        timeout=30,
    ).json()
    if "access_token" not in short:
        sys.exit(f"error: code exchange failed — {short}")

    long = requests.get(
        "https://graph.instagram.com/access_token",
        params={
            "grant_type": "ig_exchange_token",
            "client_secret": _env("IG_APP_SECRET"),
            "access_token": short["access_token"],
        },
        timeout=30,
    ).json()
    if "access_token" not in long:
        sys.exit(f"error: long-lived exchange failed — {long}")

    return {"user_id": str(short.get("user_id", "")), "access_token": long["access_token"],
            "expires_in": long.get("expires_in", 0)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", action="store_true", help="print the authorise URL to open")
    group.add_argument("--code", help="the code Instagram put in the redirect URL")
    parser.add_argument("--handle", help="account handle, to label the output variables")
    args = parser.parse_args()

    if args.url:
        print(authorize_url())
        return 0

    result = exchange(args.code)
    handle = args.handle or "YOUR_HANDLE"
    prefix = "IG_" + "".join(c if c.isalnum() else "_" for c in handle).upper()
    print(f"\nvalid for {int(result['expires_in']) // 86400} days — add to your .env:\n")
    print(f"{prefix}_USER_ID={result['user_id']}")
    print(f"{prefix}_TOKEN={result['access_token']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
