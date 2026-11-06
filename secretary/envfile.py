"""Rewrite values in an .env file without ever showing them.

Used by `refresh-tokens --write` so a renewed Instagram token goes straight
from the API into .env: nothing printed, nothing logged, no person in the loop.
Tokens lapsed on 2026-11-02 because the monthly manual refresh never happened.
"""

from __future__ import annotations

import os
import tempfile


def set_values(path: str, updates: dict[str, str]) -> None:
    """Replace `KEY=...` lines for each key in updates; append keys not present.

    Every other line is kept byte for byte. The file is replaced atomically and
    keeps mode 0600, so a crash mid-write never leaves a half-written .env.
    """
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    pending = dict(updates)
    out: list[str] = []
    for line in lines:
        key = line.split("=", 1)[0].strip()
        if "=" in line and key in pending:
            out.append(f"{key}={pending.pop(key)}")
        else:
            out.append(line)
    out.extend(f"{k}={v}" for k, v in pending.items())

    directory = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".env.")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write("\n".join(out) + "\n")
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
