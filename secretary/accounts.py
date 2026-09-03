"""Account configuration, read from the environment.

Each account needs a token, keyed by its handle with non-alphanumeric
characters folded to underscores:

    IG_ACCOUNTS=anova.autismo,pankeka.app
    IG_ANOVA_AUTISMO_TOKEN=...
    IG_PANKEKA_APP_TOKEN=...

A matching _USER_ID may also be set and is recorded, but nothing depends on
it — the API is addressed as "me".

Tokens are read from the process environment only, never from a file in the
repository. On a VPS, keep them in an .env readable by the service user alone.
"""

from __future__ import annotations

import os
import re

from .channels.instagram import Account

DEFAULT_API_VERSION = "v23.0"


def _env_prefix(handle: str) -> str:
    return "IG_" + re.sub(r"[^A-Za-z0-9]+", "_", handle).upper()


def load_accounts() -> dict[str, Account]:
    """Build the account map from the environment, failing loudly on gaps."""
    handles = [h.strip() for h in os.environ.get("IG_ACCOUNTS", "").split(",") if h.strip()]
    if not handles:
        raise RuntimeError("IG_ACCOUNTS is empty — list the handles the secretary manages")

    api_version = os.environ.get("IG_API_VERSION", DEFAULT_API_VERSION)
    accounts: dict[str, Account] = {}
    missing: list[str] = []

    for handle in handles:
        prefix = _env_prefix(handle)
        token = os.environ.get(f"{prefix}_TOKEN")
        if not token:
            missing.append(f"{prefix}_TOKEN (for {handle})")
            continue
        accounts[handle] = Account(
            handle=handle,
            access_token=token,
            api_version=api_version,
            user_id=os.environ.get(f"{prefix}_USER_ID", ""),
        )

    if missing:
        raise RuntimeError("missing credentials:\n  " + "\n  ".join(missing))
    return accounts


def load_account(handle: str) -> Account:
    accounts = load_accounts()
    if handle not in accounts:
        known = ", ".join(sorted(accounts)) or "none configured"
        raise RuntimeError(f"unknown account {handle!r} — configured accounts: {known}")
    return accounts[handle]
