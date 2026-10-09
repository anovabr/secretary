"""Finds the post to publish today.

One post per entry under media/<handle>/, published one a day as a queue:
the first entry that has never gone out, carousels in name order with a reel
after every two of them. Only when everything has gone out once does it come
back round, oldest publication first. What went out, and when, is kept in
`.secretary-published.json` beside media/ — nothing repeats while something
new is waiting, and adding a folder never reshuffles the rest.

An entry is either a folder or a loose video file, because that is how the two
kinds arrive: carousels as `post-NN-slug/` folders of slides, reels as a
single `video_something.mp4` sitting beside them. Both are dropped in as they
are.

So: a loose video file is a reel. A folder holding a video is a reel. A folder
holding images is a carousel, or a single post when there is only one.
Nothing declares which — the files decide.

Stories are loose images named `story-NN-slug.png`, one a day. A story whose
name ends with a post's slug (`story-03-artigo-mascaramento` and
`post-50-mascaramento`) announces that post and goes out only on its day; the
others take turns.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import quote

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}
# Instagram ingests MP4 and MOV for reels (H.264 video, AAC audio). Anything
# else has to be converted before it gets here; the container would fail at
# Meta's end with a message nobody sees until the report.
VIDEO_SUFFIXES = {".mp4", ".mov"}
CAPTION_FILE = "caption.txt"
# A reel's thumbnail. Optional: without it Instagram picks a frame itself.
COVER_STEM = "cover"

# Instagram fetches media over HTTP, so the images must be publicly reachable.
# Raw GitHub serves any public repository directly, which is why the media
# stays public even when the code does not.
#
# Set IG_MEDIA_BASE to move the images elsewhere — your own domain, say — and
# nothing else has to change. Renaming the repository is the same one line.
DEFAULT_BASE = os.environ.get(
    "IG_MEDIA_BASE",
    "https://raw.githubusercontent.com/anovabr/secretary/main",
)

# Video is served from somewhere else, because raw GitHub hands every file back
# as application/octet-stream with nosniff. Instagram's ingest reads the
# Content-Type and refuses a reel that arrives as a generic blob — the
# container fails at Meta's end, minutes after the run has moved on. nginx on
# this box serves the same folder as video/mp4, so IG_VIDEO_BASE points there.
#
# Unset, this falls back to DEFAULT_BASE and reels behave exactly as images do.
DEFAULT_VIDEO_BASE = os.environ.get("IG_VIDEO_BASE", "") or DEFAULT_BASE


@dataclass(frozen=True)
class Post:
    folder: Path
    image_urls: list[str]
    caption: str
    video_url: str | None = None
    cover_url: str | None = None

    @property
    def name(self) -> str:
        # For a loose reel this is the file without its extension, which is
        # what the report should say: "Reel - Camuflamento", not "...mp4".
        return self.folder.stem if self.folder.is_file() else self.folder.name

    @property
    def is_reel(self) -> bool:
        return self.video_url is not None

    @property
    def is_carousel(self) -> bool:
        # A reel is never a carousel, whatever images sit beside the video —
        # those are its cover, not slides.
        return not self.is_reel and len(self.image_urls) > 1


def _publishable(suffix: str) -> bool:
    return suffix.lower() in IMAGE_SUFFIXES or suffix.lower() in VIDEO_SUFFIXES


def _is_video(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in VIDEO_SUFFIXES


def _url(base: str, handle: str, *parts: str) -> str:
    """A public URL for a file under media/<handle>/.

    Every part is percent-encoded: reels arrive named the way the editor
    exported them — `Reel - Como o Camuflamento Esconde.mp4` — and a raw space
    in a URL is not a URL. Instagram would fetch nothing and the container
    would fail minutes later, at Meta's end.
    """
    tail = "/".join(quote(p) for p in parts)
    return f"{base.rstrip('/')}/media/{handle}/{tail}"


def post_folders(handle: str, root: Path | str = "media") -> list[Path]:
    """Every post prepared for this account, in name order.

    A post is a folder of slides or a loose video file — the two shapes the
    Windows machine produces. Name order is the rotation, so each takes its
    turn where its name puts it and adding one moves nothing else.
    """
    account = Path(root) / handle
    if not account.is_dir():
        return []
    return sorted(
        f for f in account.iterdir()
        if (f.is_dir() and any(_publishable(i.suffix) for i in f.iterdir()))
        or _is_video(f)
    )


def load_post(folder: Path, handle: str, base_url: str = DEFAULT_BASE,
              video_base_url: str | None = None) -> Post:
    video_base = video_base_url or DEFAULT_VIDEO_BASE

    if _is_video(folder):
        # A loose reel. Its caption and cover are siblings sharing its name,
        # so `Reel - Camuflamento.mp4` is captioned by
        # `Reel - Camuflamento.txt` and covered by `Reel - Camuflamento.jpg`.
        # Both optional: without a caption it publishes bare, without a cover
        # Instagram picks a frame.
        stem = folder.stem
        caption_file = folder.with_suffix(".txt")
        caption = caption_file.read_text(encoding="utf-8").strip() if caption_file.is_file() else ""
        cover = next(
            (folder.with_suffix(ext) for ext in (".jpg", ".jpeg", ".png")
             if folder.with_suffix(ext).is_file()),
            None,
        )
        return Post(
            folder=folder,
            image_urls=[],
            caption=caption,
            video_url=_url(video_base, handle, folder.name),
            cover_url=_url(base_url, handle, cover.name) if cover else None,
        )

    images = sorted(
        f for f in folder.iterdir() if f.suffix.lower() in IMAGE_SUFFIXES
    )
    videos = sorted(
        f for f in folder.iterdir() if f.suffix.lower() in VIDEO_SUFFIXES
    )

    caption_path = folder / CAPTION_FILE
    caption = caption_path.read_text(encoding="utf-8").strip() if caption_path.exists() else ""

    # The URL describes where the file sits in the repository, not where it
    # happens to sit on this disk. Deriving it from the local path leaks
    # absolute paths into the URL whenever the checkout is not the working
    # directory — and Instagram would simply fail to fetch it.
    if videos:
        # One video is one reel. A second video in the same folder is a
        # mistake rather than a second post, so the first in name order wins
        # and the rest are ignored.
        cover = next((i for i in images if i.stem.lower() == COVER_STEM), None)
        return Post(
            folder=folder,
            image_urls=[],
            caption=caption,
            video_url=_url(video_base, handle, folder.name, videos[0].name),
            cover_url=_url(base_url, handle, folder.name, cover.name) if cover else None,
        )

    if len(images) > 10:
        # Publishing 11 would fail at the API; taking the first 10 keeps the
        # day's post going out and the report says what was dropped.
        images = images[:10]

    return Post(
        folder=folder,
        image_urls=[_url(base_url, handle, folder.name, i.name) for i in images],
        caption=caption,
    )


PUBLISHED_FILE = ".secretary-published.json"
REELS_EVERY = 2  # carrosséis entre um reel e outro


def published_log(root: Path | str = "media") -> Path:
    """Where the record of publications lives: beside media/, never inside it."""
    return Path(root).resolve().parent / PUBLISHED_FILE


def _load_log(log: Path) -> dict:
    try:
        return json.loads(log.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def record_published(handle: str, name: str, today: date | None = None,
                     root: Path | str = "media") -> None:
    """Note that `name` went out today, so the queue moves on."""
    log = published_log(root)
    data = _load_log(log)
    data.setdefault(handle, {})[name] = (today or date.today()).isoformat()
    log.write_text(json.dumps(data, indent=1, ensure_ascii=False, sort_keys=True))


def _entry_name(path: Path) -> str:
    return path.stem if path.is_file() else path.name


def _is_reel_entry(path: Path) -> bool:
    return _is_video(path) or (path.is_dir() and any(_is_video(f) for f in path.iterdir()))


def _queue(entries: list[Path]) -> list[Path]:
    """The order a fresh account would publish in: a reel after every REELS_EVERY carousels."""
    posts = [e for e in entries if not _is_reel_entry(e)]
    reels = [e for e in entries if _is_reel_entry(e)]
    out: list[Path] = []
    while posts or reels:
        out += posts[:REELS_EVERY]; posts = posts[REELS_EVERY:]
        out += reels[:1]; reels = reels[1:]
    return out


def _pick(entries: list[Path], done: dict, today: date) -> Path | None:
    """Today's own if already published today; else the first new one; else the oldest."""
    if not entries:
        return None
    by_name = {_entry_name(e): e for e in entries}
    for name, day in done.items():
        if day == today.isoformat() and name in by_name:
            return by_name[name]
    for e in entries:
        if _entry_name(e) not in done:
            return e
    return min(entries, key=lambda e: (done[_entry_name(e)], entries.index(e)))


def post_for(handle: str, today: date | None = None, root: Path | str = "media",
             base_url: str = DEFAULT_BASE,
             video_base_url: str | None = None) -> Post | None:
    """The post due today, or None if this account has no posts prepared."""
    today = today or date.today()
    done = _load_log(published_log(root)).get(handle, {})
    entries = post_folders(handle, root)
    waiting = [e for e in entries if _entry_name(e) not in done]
    reels = [e for e in waiting if _is_reel_entry(e)]
    posts = [e for e in waiting if not _is_reel_entry(e)]
    # depois de REELS_EVERY carrosséis seguidos, o reel que espera vai na frente
    is_reel = {_entry_name(e): _is_reel_entry(e) for e in entries}
    recent = [n for n, _ in sorted(done.items(), key=lambda kv: kv[1], reverse=True) if n in is_reel]
    reel_due = len(recent) >= REELS_EVERY and not any(is_reel[n] for n in recent[:REELS_EVERY])
    waiting = reels + posts if reel_due or not posts else posts + reels
    entry = _pick(waiting + [e for e in entries if _entry_name(e) in done], done, today)
    if entry is None:
        return None
    return load_post(entry, handle, base_url, video_base_url)


@dataclass(frozen=True)
class Story:
    path: Path
    image_url: str

    @property
    def name(self) -> str:
        return self.path.stem


def story_files(handle: str, root: Path | str = "media") -> list[Path]:
    account = Path(root) / handle
    if not account.is_dir():
        return []
    return sorted(f for f in account.iterdir()
                  if f.is_file() and f.name.startswith("story-") and f.suffix.lower() in IMAGE_SUFFIXES)


def _slug(folder_name: str) -> str:
    """`post-50-mascaramento` -> `mascaramento`."""
    parts = folder_name.split("-", 2)
    return parts[2] if len(parts) == 3 and parts[0] == "post" and parts[1].isdigit() else folder_name


def story_for(handle: str, post: Post | None, today: date | None = None,
              root: Path | str = "media", base_url: str = DEFAULT_BASE) -> Story | None:
    """Today's story: the one announcing today's post, or the next of the rest."""
    today = today or date.today()
    stories = story_files(handle, root)
    if not stories:
        return None
    slugs = {_slug(f.name) for f in post_folders(handle, root) if f.is_dir()}
    tied = {s: next((g for g in slugs if s.stem.endswith("-" + g)), None) for s in stories}
    pick = None
    if post is not None:
        own = _slug(post.name)
        pick = next((s for s in stories if tied[s] == own), None)
    if pick is None:
        free = [s for s in stories if tied[s] is None]
        done = _load_log(published_log(root)).get(handle, {})
        pick = _pick(free, done, today)
    if pick is None:
        return None
    return Story(pick, _url(base_url, handle, pick.name))
