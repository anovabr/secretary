"""Instagram Business channel — publish posts, read comments, post replies.

Built on the Instagram API with Instagram Login (graph.instagram.com), which
needs an Instagram Business or Creator account. One Meta app can serve several
accounts; each account authorises separately and gets its own long-lived token.

Note on media: Instagram fetches the image or video from a URL you supply, so
`image_url` and `video_url` must be publicly reachable over HTTPS. There is no
direct file upload.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Iterator

import requests

GRAPH = "https://graph.instagram.com"

# Container processing is async for video; these bound the wait.
_POLL_INTERVAL_S = 5
_POLL_TIMEOUT_S = 300

# Meta only accepts a free-form reply within 24h of the person's last message.
# We stop a little short of the edge so a slow run doesn't post into a closed window.
REPLY_WINDOW = timedelta(hours=23, minutes=30)


class InstagramError(RuntimeError):
    """An error reported by the Instagram API, with Meta's own message kept intact."""


@dataclass(frozen=True)
class Account:
    """One authorised Instagram account."""

    handle: str           # e.g. "anova.autismo" — how the daily list refers to it
    access_token: str     # long-lived token, ~60 days
    api_version: str = "v23.0"
    # The id shown in the app dashboard. Kept only so a .env can record which
    # account a token belongs to; the API is addressed as "me" and reports its
    # own id, which lives in a different identifier space and is the one that
    # matters. Nothing here depends on this value.
    user_id: str = ""

    def __repr__(self) -> str:  # keep tokens out of tracebacks and logs
        return f"Account(handle={self.handle!r})"


class Instagram:
    def __init__(self, account: Account, *, dry_run: bool = False):
        self.account = account
        self.dry_run = dry_run
        self._base = f"{GRAPH}/{account.api_version}"
        self._session = requests.Session()
        self._me_id: str | None = None

    @property
    def me_id(self) -> str:
        """The account's id *as this API reports it*, fetched once.

        The id shown in the app dashboard (17841...) and the id the API returns
        (a longer app-scoped one) are different identifier spaces for the same
        account. Only the API's own id can be compared against the sender id on
        a message, so that is the one we ask for rather than the configured one.
        """
        if self._me_id is None:
            self._me_id = str(self._get("me", fields="id")["id"])
        return self._me_id

    # ---------- transport ----------

    def _request(self, method: str, path: str, **params: Any) -> dict:
        url = path if path.startswith("http") else f"{self._base}/{path}"
        params["access_token"] = self.account.access_token
        response = self._session.request(method, url, params=params, timeout=30)
        try:
            payload = response.json()
        except ValueError:
            raise InstagramError(f"{method} {path} returned non-JSON ({response.status_code})")
        if "error" in payload:
            err = payload["error"]
            raise InstagramError(
                f"{err.get('type', 'Error')} {err.get('code', '')}: {err.get('message', payload)}".strip()
            )
        return payload

    def _get(self, path: str, **params: Any) -> dict:
        return self._request("GET", path, **params)

    def _post_json(self, path: str, body: dict) -> dict:
        """POST with a JSON body — the messaging endpoints require it."""
        if self.dry_run:
            print(f"  [dry-run] POST {path} {body}")
            return {"message_id": "dry-run"}
        response = self._session.post(
            f"{self._base}/{path}",
            params={"access_token": self.account.access_token},
            json=body,
            timeout=30,
        )
        payload = response.json()
        if "error" in payload:
            err = payload["error"]
            raise InstagramError(
                f"{err.get('type', 'Error')} {err.get('code', '')}: {err.get('message', payload)}".strip()
            )
        return payload

    def _post(self, path: str, **params: Any) -> dict:
        if self.dry_run:
            redacted = {k: v for k, v in params.items() if k != "access_token"}
            print(f"  [dry-run] POST {path} {redacted}")
            return {"id": "dry-run"}
        return self._request("POST", path, **params)

    # ---------- identity ----------

    def whoami(self) -> dict:
        """Confirm the token works and report which account it belongs to."""
        return self._get("me", fields="id,username,account_type,followers_count")

    def refresh_token(self) -> dict:
        """Extend a long-lived token by another 60 days.

        The token must be at least 24 hours old. Run this well before expiry —
        once a token lapses the whole OAuth flow has to be repeated by hand.
        """
        return self._get(
            f"{GRAPH}/refresh_access_token", grant_type="ig_refresh_token"
        )

    # ---------- publishing ----------

    def publish_image(self, image_url: str, caption: str = "") -> str:
        """Publish a single image. Returns the published media id."""
        container = self._post(
            "me/media", image_url=image_url, caption=caption
        )["id"]
        self._await_container(container)
        return self._publish(container)

    def publish_reel(self, video_url: str, caption: str = "", cover_url: str | None = None) -> str:
        """Publish a reel. Returns the published media id."""
        params: dict[str, Any] = {"media_type": "REELS", "video_url": video_url, "caption": caption}
        if cover_url:
            params["cover_url"] = cover_url
        container = self._post("me/media", **params)["id"]
        self._await_container(container)
        return self._publish(container)

    def publish_carousel(self, image_urls: list[str], caption: str = "") -> str:
        """Publish 2-10 images as a carousel. Returns the published media id."""
        if not 2 <= len(image_urls) <= 10:
            raise ValueError(f"a carousel holds 2-10 images, got {len(image_urls)}")
        children = [
            self._post("me/media", image_url=url, is_carousel_item="true")["id"]
            for url in image_urls
        ]
        container = self._post(
            "me/media",
            media_type="CAROUSEL",
            children=",".join(children),
            caption=caption,
        )["id"]
        self._await_container(container)
        return self._publish(container)

    def _publish(self, container_id: str) -> str:
        return self._post("me/media_publish", creation_id=container_id)["id"]

    def _await_container(self, container_id: str) -> None:
        """Block until a container is ready to publish.

        Instagram fetches the media from our URL after the container is
        created, and publishing before that finishes fails with error 9007,
        "Media ID is not available". Images usually take seconds, video
        minutes — the first live run lost its post to this, so every kind of
        container waits.
        """
        if self.dry_run:
            return
        deadline = time.monotonic() + _POLL_TIMEOUT_S
        while time.monotonic() < deadline:
            status = self._get(container_id, fields="status_code,status").get("status_code")
            if status == "FINISHED":
                return
            if status == "ERROR":
                detail = self._get(container_id, fields="status").get("status", "")
                raise InstagramError(f"container {container_id} failed to process: {detail}")
            time.sleep(_POLL_INTERVAL_S)
        raise InstagramError(f"container {container_id} still processing after {_POLL_TIMEOUT_S}s")

    # ---------- reading ----------

    def recent_media(self, limit: int = 10) -> list[dict]:
        return self._get(
            "me/media",
            fields="id,caption,permalink,timestamp,media_type,comments_count",
            limit=limit,
        ).get("data", [])

    def comments(self, media_id: str) -> list[dict]:
        """Comments on one of your posts, newest first."""
        return self._get(
            f"{media_id}/comments",
            fields="id,text,username,timestamp,hidden,replies{id,text,username,timestamp}",
        ).get("data", [])

    def unanswered_comments(self, limit: int = 10) -> Iterator[dict]:
        """Comments across recent posts that nobody from the account has replied to.

        This is the queue a daily run works through: each item carries the media
        it belongs to, so a reply can be attributed back to the right post.
        """
        me = self.account.handle
        for media in self.recent_media(limit=limit):
            if not media.get("comments_count"):
                continue
            for comment in self.comments(media["id"]):
                if comment.get("username") == me:
                    continue
                replies = comment.get("replies", {}).get("data", [])
                if any(r.get("username") == me for r in replies):
                    continue
                yield {**comment, "media_id": media["id"], "permalink": media.get("permalink")}

    # ---------- responding ----------

    def reply_to_comment(self, comment_id: str, message: str) -> str:
        return self._post(f"{comment_id}/replies", message=message)["id"]

    def hide_comment(self, comment_id: str, hidden: bool = True) -> None:
        self._post(comment_id, hide="true" if hidden else "false")


    # ---------- direct messages ----------

    def conversations(self, limit: int = 25) -> list[dict]:
        """Open DM threads, most recently active first."""
        return self._get(
            "me/conversations",
            platform="instagram",
            fields="id,updated_time,participants",
            limit=limit,
        ).get("data", [])

    def messages(self, conversation_id: str, limit: int = 25) -> list[dict]:
        """Messages in one thread, newest first."""
        return self._get(
            conversation_id,
            fields=f"messages.limit({limit}){{id,created_time,from,to,message}}",
        ).get("messages", {}).get("data", [])

    def unanswered_threads(self, limit: int = 25) -> list[dict]:
        """DM threads where the last word was theirs, not ours.

        Each result carries `within_window`: False means Meta will reject a
        free-form reply because more than 24 hours have passed. Those threads
        still need a human, so they are returned rather than silently dropped.
        """
        pending = []
        for conversation in self.conversations(limit=limit):
            history = self.messages(conversation["id"], limit=10)
            if not history:
                continue
            latest = history[0]
            sender = latest.get("from", {})
            if str(sender.get("id")) == self.me_id:
                continue  # we spoke last; nothing owed
            age = _age_of(latest.get("created_time", ""))
            pending.append({
                "conversation_id": conversation["id"],
                "sender_id": sender.get("id"),
                "sender": sender.get("username", "?"),
                "text": latest.get("message", ""),
                "created_time": latest.get("created_time"),
                "within_window": age is not None and age < REPLY_WINDOW,
                "age": age,
            })
        return pending

    def send_message(self, recipient_id: str, text: str) -> str:
        """Send a DM. Only valid inside the 24-hour window."""
        result = self._post_json(
            "me/messages",
            {"recipient": {"id": str(recipient_id)}, "message": {"text": text}},
        )
        return result.get("message_id", "")


# "+0000" -> "+00:00". datetime.fromisoformat only accepts the colon-less form
# from Python 3.11, and Instagram always sends it that way — so on 3.10 every
# timestamp failed to parse, every message looked ageless, and the 24-hour
# window was reported as closed for even the freshest DM.
_OFFSET_NO_COLON = re.compile(r"([+-]\d{2})(\d{2})$")


def _age_of(created_time: str) -> timedelta | None:
    """How long ago a message arrived, or None if the timestamp is unparseable."""
    if not created_time:
        return None
    normalised = _OFFSET_NO_COLON.sub(r"\1:\2", created_time.strip().replace("Z", "+00:00"))
    try:
        stamp = datetime.fromisoformat(normalised)
    except ValueError:
        return None
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) - stamp
