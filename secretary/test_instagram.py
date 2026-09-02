"""Tests for the Instagram channel, run against a stubbed transport.

    python -m secretary.test_instagram
"""

import unittest
from unittest.mock import patch

from datetime import datetime, timedelta, timezone

from .channels.instagram import Account, Instagram, InstagramError, _age_of

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


def _ago(**kw):
    return (datetime.now(timezone.utc) - timedelta(**kw)).isoformat().replace("+00:00", "+0000")


CONVERSATIONS = {"data": [{"id": "t1"}, {"id": "t2"}, {"id": "t3"}]}

THREADS = {
    # they wrote last, 2 hours ago -> answerable
    "t1": [{"id": "m1", "created_time": _ago(hours=2), "message": "Qual a idade indicada?",
            "from": {"id": "999", "username": "mae_do_pedro"}}],
    # they wrote last, 3 days ago -> outside the window, needs a human
    "t2": [{"id": "m2", "created_time": _ago(days=3), "message": "Vocês atendem em Niterói?",
            "from": {"id": "888", "username": "carlos.ferreira"}}],
    # we wrote last -> nothing owed
    "t3": [{"id": "m3", "created_time": _ago(hours=1), "message": "Às ordens!",
            "from": {"id": ACCOUNT.user_id, "username": "anova.autismo"}}],
}


class TestDirectMessages(unittest.TestCase):
    def setUp(self):
        self.sent = []
        patcher = patch.object(Instagram, "_request", side_effect=self._route)
        self.addCleanup(patcher.stop)
        patcher.start()

    def _route(self, method, path, **params):
        if path == "me/conversations":
            return CONVERSATIONS
        if path in THREADS:
            return {"messages": {"data": THREADS[path]}}
        return {}

    def test_only_threads_awaiting_us(self):
        pending = Instagram(ACCOUNT).unanswered_threads()
        self.assertEqual([p["conversation_id"] for p in pending], ["t1", "t2"])

    def test_window_is_flagged_not_hidden(self):
        by_id = {p["conversation_id"]: p for p in Instagram(ACCOUNT).unanswered_threads()}
        self.assertTrue(by_id["t1"]["within_window"])
        self.assertFalse(by_id["t2"]["within_window"])

    def test_sender_is_carried_for_the_report(self):
        pending = Instagram(ACCOUNT).unanswered_threads()
        self.assertEqual(pending[0]["sender"], "mae_do_pedro")
        self.assertEqual(pending[0]["text"], "Qual a idade indicada?")


class TestSendMessage(unittest.TestCase):
    def test_dry_run_sends_nothing(self):
        with patch("requests.Session.post") as post:
            Instagram(ACCOUNT, dry_run=True).send_message("999", "Olá!")
            post.assert_not_called()

    def test_body_is_json_not_query_params(self):
        with patch("requests.Session.post") as post:
            post.return_value.json.return_value = {"message_id": "mid.1"}
            Instagram(ACCOUNT).send_message("999", "Bom dia!")
        _, kwargs = post.call_args
        self.assertEqual(kwargs["json"], {"recipient": {"id": "999"}, "message": {"text": "Bom dia!"}})
        self.assertEqual(kwargs["params"], {"access_token": "tok"})


class TestAgeParsing(unittest.TestCase):
    def test_handles_z_suffix_and_offset(self):
        for stamp in ("2026-09-01T10:00:00Z", "2026-09-01T10:00:00+0000", "2026-09-01T10:00:00+00:00"):
            self.assertIsNotNone(_age_of(stamp), stamp)

    def test_unparseable_is_none_not_a_crash(self):
        self.assertIsNone(_age_of("last tuesday"))
        self.assertIsNone(_age_of(""))

    def test_naive_timestamp_assumed_utc(self):
        self.assertIsNotNone(_age_of("2026-09-01T10:00:00"))




class TestReport(unittest.TestCase):
    def _report(self):
        from .report import Report
        return Report(datetime(2026, 9, 3, 7, 41))

    def test_empty_report_says_so(self):
        self.assertIn("Nada a relatar", self._report().render())

    def test_singular_and_plural_agree_in_portuguese(self):
        from .report import Report
        r = Report(datetime(2026, 9, 3, 7, 41))
        s = r.section("Teste")
        r.feito(s, "uma coisa")
        self.assertIn("1 tarefa concluída", r.render())
        r.feito(s, "outra coisa")
        self.assertIn("2 tarefas concluídas", r.render())

    def test_attention_items_are_repeated_at_the_end(self):
        from .report import Report
        r = Report(datetime(2026, 9, 3, 7, 41))
        s = r.section("Instagram")
        r.feito(s, "publicado")
        r.atencao(s, "mensagem fora da janela", "@alguem, há 3 dias")
        rendered = r.render()
        self.assertIn("PRECISAM DE VOCÊ", rendered)
        self.assertEqual(rendered.count("mensagem fora da janela"), 2)
        self.assertNotIn("publicado", rendered.split("PRECISAM DE VOCÊ")[1])

    def test_clean_run_has_no_action_block(self):
        from .report import Report
        r = Report(datetime(2026, 9, 3, 7, 41))
        s = r.section("Instagram")
        r.feito(s, "publicado")
        self.assertNotIn("PRECISAM DE VOCÊ", r.render())

    def test_failures_also_reach_the_action_block(self):
        from .report import Report, Status
        r = Report(datetime(2026, 9, 3, 7, 41))
        s = r.section("Painel")
        r.falhou(s, "painel fora do ar", "timeout após 30s")
        self.assertIn("PRECISAM DE VOCÊ", r.render())
        self.assertEqual(r.counts()[Status.FALHOU], 1)

    def test_weekday_and_month_are_portuguese(self):
        self.assertIn("quinta-feira, 3 de setembro de 2026", self._report().render())

    def test_demo_renders(self):
        from .demo_report import build
        self.assertIn("RELATÓRIO DA SECRETÁRIA", build().render())


class TestReportSections(unittest.TestCase):
    def _r(self):
        from .report import Report
        return Report(datetime(2026, 9, 3, 7, 41))

    def test_same_title_is_one_section(self):
        r = self._r()
        a = r.section("Instagram · anova.autismo")
        b = r.section("Instagram · anova.autismo")
        self.assertIs(a, b)
        self.assertEqual(len(r.sections), 1)

    def test_heading_appears_once_however_many_steps_write_to_it(self):
        r = self._r()
        for what in ("publicado", "mensagens", "comentários"):
            r.feito(r.section("Instagram · anova.autismo"), what)
        self.assertEqual(r.render().count("INSTAGRAM · ANOVA.AUTISMO"), 1)

    def test_different_titles_stay_separate(self):
        r = self._r()
        r.section("Instagram · anova.autismo")
        r.section("Instagram · pankeka.app")
        self.assertEqual(len(r.sections), 2)

    def test_action_items_name_their_account(self):
        r = self._r()
        for handle in ("anova.autismo", "pankeka.app"):
            r.atencao(r.section(f"Instagram · {handle}"), "1 mensagem aguardando resposta")
        tail = r.render().split("PRECISAM DE VOCÊ")[1]
        self.assertIn("Instagram · anova.autismo — 1 mensagem", tail)
        self.assertIn("Instagram · pankeka.app — 1 mensagem", tail)


if __name__ == "__main__":
    unittest.main(verbosity=2)
