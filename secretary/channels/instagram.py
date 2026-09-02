"""Instagram Business channel — publish posts, read comments, post replies.

Built on the Instagram API with Instagram Login (graph.instagram.com), which
needs an Instagram Business or Creator account. One Meta app can serve several
accounts; each account authorises separately and gets its own long-lived token.

Note on media: Instagram fetches the image or video from a URL you supply, so
`image_url` and `video_url` must be publicly reachable over HTTPS. There is no
direct file upload.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Iterator

import requests

GRAPH = "https://graph.instagram.com"

# Container processing is async for video; these bound the wait.
_POLL_INTERVAL_S = 5
_POLL_TIMEOUT_S = 300


class InstagramError(RuntimeError):
    """An error reported by the Instagram API, with Meta's own message kept intact."""


@dataclass(frozen=True)
class Account:
    """One authorised Instagram account."""

    handle: str           # e.g. "anova.autismo" — how the daily list refers to it
    user_id: str          # Instagram-scoped user id
    access_token: str     # long-lived token, ~60 days
    api_version: str = "v23.0"

    def __repr__(self) -> str:  # keep tokens out of tracebacks and logs
        return f"Account(handle={self.handle!r}, user_id={self.user_id!r})"


class Instagram:
    def __init__(self, account: Account, *, dry_run: bool = False):
        self.account = account
        self.dry_run = dry_run
        self._base = f"{GRAPH}/{account.api_version}"
        self._session = requests.Session()

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
            f"{self.account.user_id}/media", image_url=image_url, caption=caption
        )["id"]
        return self._publish(container)

    def publish_reel(self, video_url: str, caption: str = "", cover_url: str | None = None) -> str:
        """Publish a reel. Returns the published media id."""
        params: dict[str, Any] = {"media_type": "REELS", "video_url": video_url, "caption": caption}
        if cover_url:
            params["cover_url"] = cover_url
        container = self._post(f"{self.account.user_id}/media", **params)["id"]
        self._await_container(container)
        return self._publish(container)

    def publish_carousel(self, image_urls: list[str], caption: str = "") -> str:
        """Publish 2-10 images as a carousel. Returns the published media id."""
        if not 2 <= len(image_urls) <= 10:
            raise ValueError(f"a carousel holds 2-10 images, got {len(image_urls)}")
        children = [
            self._post(f"{self.account.user_id}/media", image_url=url, is_carousel_item="true")["id"]
            for url in image_urls
        ]
        container = self._post(
            f"{self.account.user_id}/media",
            media_type="CAROUSEL",
            children=",".join(children),
            caption=caption,
        )["id"]
        return self._publish(container)

    def _publish(self, container_id: str) -> str:
        return self._post(f"{self.account.user_id}/media_publish", creation_id=container_id)["id"]

    def _await_container(self, container_id: str) -> None:
        """Block until a video container finishes transcoding."""
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
            f"{self.account.user_id}/media",
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
