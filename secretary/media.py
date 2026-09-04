"""Finds the post to publish today.

One folder per post under media/<handle>/, published in folder-name order, one
a day, cycling round when they run out. Twenty folders is twenty days.

The rotation is derived from the date rather than stored, so it survives the
state file being lost and never publishes twice for the same day.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}
CAPTION_FILE = "caption.txt"

# Instagram fetches media over HTTP, so the images must be publicly reachable.
# Raw GitHub serves any public repository directly, which is why the media
# stays public even when the code does not.
#
# Set IG_MEDIA_BASE to move the images elsewhere — your own domain, say — and
# nothing else has to change. Renaming the repository is the same one line.
DEFAULT_BASE = os.environ.get(
    "IG_MEDIA_BASE",
    "https://raw.githubusercontent.com/anovabr/secretary/"
    "claude/instagram-account-integration-4hoqk3",
)


@dataclass(frozen=True)
class Post:
    folder: Path
    image_urls: list[str]
    caption: str

    @property
    def name(self) -> str:
        return self.folder.name

    @property
    def is_carousel(self) -> bool:
        return len(self.image_urls) > 1


def post_folders(handle: str, root: Path | str = "media") -> list[Path]:
    """Every folder holding at least one image, in name order."""
    account = Path(root) / handle
    if not account.is_dir():
        return []
    return sorted(
        f for f in account.iterdir()
        if f.is_dir() and any(i.suffix.lower() in IMAGE_SUFFIXES for i in f.iterdir())
    )


def load_post(folder: Path, handle: str, base_url: str = DEFAULT_BASE) -> Post:
    images = sorted(
        f for f in folder.iterdir() if f.suffix.lower() in IMAGE_SUFFIXES
    )
    if len(images) > 10:
        # Publishing 11 would fail at the API; taking the first 10 keeps the
        # day's post going out and the report says what was dropped.
        images = images[:10]

    caption_path = folder / CAPTION_FILE
    caption = caption_path.read_text(encoding="utf-8").strip() if caption_path.exists() else ""

    # The URL describes where the file sits in the repository, not where it
    # happens to sit on this disk. Deriving it from the local path leaks
    # absolute paths into the URL whenever the checkout is not the working
    # directory — and Instagram would simply fail to fetch it.
    prefix = f"{base_url.rstrip('/')}/media/{handle}/{folder.name}"
    return Post(
        folder=folder,
        image_urls=[f"{prefix}/{i.name}" for i in images],
        caption=caption,
    )


def post_for(handle: str, today: date | None = None, root: Path | str = "media",
             base_url: str = DEFAULT_BASE) -> Post | None:
    """The post due today, or None if this account has no posts prepared."""
    folders = post_folders(handle, root)
    if not folders:
        return None
    index = (today or date.today()).toordinal() % len(folders)
    return load_post(folders[index], handle, base_url)
