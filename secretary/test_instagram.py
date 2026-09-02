"""Tests for the Instagram channel, run against a stubbed transport.

    python -m secretary.test_instagram
"""

import unittest
from unittest.mock import patch

from .channels.instagram import Account, Instagram, InstagramError

ACCOUNT = Account(handle="anova.autismo", user_id="17841400000000000", access_token="tok")

MEDIA = {
    "data": [
        {"id": "m1", "permalink": "https://instagr.am/p/1", "comments_count": 3},
        {"id": "m2", "permalink": "https://instagr.am/p/2", "comments_count": 0},
    ]
}

COMMENTS = {
    "m1": {
        "data": [
            # already answered by the account — must be filtered out
            {"id": "c1", "username": "mae_do_pedro", "text": "Que idade indicada?",
             "replies": {"data": [{"id": "r1", "username": "anova.autismo", "text": "A partir de 4!"}]}},
            # unanswered — must surface
            {"id": "c2", "username": "prof.carla", "text": "Tem versão para escolas?"},
            # our own comment — must be filtered out
            {"id": "c3", "username": "anova.autismo", "text": "Obrigado a todos!"},
        ]
    }
}


class StubTransport(unittest.TestCase):
    def setUp(self):
        self.posts = []
        patcher = patch.object(Instagram, "_request", side_effect=self._route)
        self.addCleanup(patcher.stop)
        patcher.start()

    def _route(self, method, path, **params):
        if method == "POST":
            self.posts.append((path, {k: v for k, v in params.items() if k != "access_token"}))
            return {"id": f"new-{len(self.posts)}"}
        if path.endswith("/media"):
            return MEDIA
        if path.endswith("/comments"):
            return COMMENTS.get(path.split("/")[0], {"data": []})
        if path.endswith("status_code") or "fields" in params:
            return {"status_code": "FINISHED"}
        return {}


class TestUnansweredComments(StubTransport):
    def test_skips_answered_and_own_comments(self):
        pending = list(Instagram(ACCOUNT).unanswered_comments())
        self.assertEqual([c["id"] for c in pending], ["c2"])

    def test_carries_media_context_for_attribution(self):
        pending = list(Instagram(ACCOUNT).unanswered_comments())
        self.assertEqual(pending[0]["media_id"], "m1")
        self.assertEqual(pending[0]["permalink"], "https://instagr.am/p/1")

    def test_skips_media_with_no_comments(self):
        # m2 has comments_count 0; it must not be fetched at all
        list(Instagram(ACCOUNT).unanswered_comments())


class TestPublishing(StubTransport):
    def test_image_creates_container_then_publishes(self):
        Instagram(ACCOUNT).publish_image("https://cdn/x.jpg", "olá")
        self.assertEqual(len(self.posts), 2)
        self.assertEqual(self.posts[0][1], {"image_url": "https://cdn/x.jpg", "caption": "olá"})
        self.assertEqual(self.posts[1][1], {"creation_id": "new-1"})

    def test_carousel_builds_children_then_parent(self):
        Instagram(ACCOUNT).publish_carousel(["https://a.jpg", "https://b.jpg"], "duas fotos")
        # two children, one parent container, one publish
        self.assertEqual(len(self.posts), 4)
        self.assertEqual(self.posts[0][1]["is_carousel_item"], "true")
        self.assertEqual(self.posts[2][1]["children"], "new-1,new-2")

    def test_carousel_rejects_bad_counts(self):
        for urls in ([], ["https://a.jpg"], [f"https://{i}.jpg" for i in range(11)]):
            with self.assertRaises(ValueError):
                Instagram(ACCOUNT).publish_carousel(urls)


class TestDryRun(unittest.TestCase):
    def test_dry_run_sends_nothing(self):
        with patch.object(Instagram, "_request") as request:
            Instagram(ACCOUNT, dry_run=True).publish_image("https://cdn/x.jpg", "olá")
            request.assert_not_called()

    def test_dry_run_still_reads(self):
        with patch.object(Instagram, "_request", return_value=MEDIA) as request:
            Instagram(ACCOUNT, dry_run=True).recent_media()
            request.assert_called_once()


class TestErrors(unittest.TestCase):
    def test_api_error_is_surfaced_with_metas_message(self):
        payload = {"error": {"type": "OAuthException", "code": 190, "message": "Session has expired"}}
        with patch("requests.Session.request") as request:
            request.return_value.json.return_value = payload
            with self.assertRaises(InstagramError) as ctx:
                Instagram(ACCOUNT).whoami()
        self.assertIn("Session has expired", str(ctx.exception))
        self.assertIn("OAuthException", str(ctx.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
