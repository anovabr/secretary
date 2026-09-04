"""Tests for the runner — chiefly its three promises: isolation, no repeats,
and that a dry run leaves no trace.

    python -m secretary.test_runner
"""

import json
import tempfile
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path

from .report import Report, Status
from .runner import DayState, Runner, Step


def _step(key, log, *, fails=False, once=True):
    def run(ctx):
        log.append(key)
        if fails:
            raise RuntimeError("painel fora do ar")
        ctx.feito(f"{key} concluído")
    return Step(key=key, title=key, run=run, once_per_day=once)


class RunnerCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.state_path = Path(self.tmp.name) / "state.json"
        self.log = []

    def _runner(self, *, dry_run=False, today=None):
        return Runner(
            Report(datetime(2026, 9, 3, 7, 0)),
            DayState(self.state_path, today=today or date(2026, 9, 3)),
            dry_run=dry_run,
        )


class TestOrderAndIsolation(RunnerCase):
    def test_steps_run_in_order(self):
        r = self._runner()
        for k in ("a", "b", "c"):
            r.add(_step(k, self.log))
        r.run_all()
        self.assertEqual(self.log, ["a", "b", "c"])

    def test_a_failing_step_does_not_stop_the_rest(self):
        r = self._runner()
        r.add(_step("post", self.log))
        r.add(_step("painel", self.log, fails=True))
        r.add(_step("pankeka", self.log))
        r.run_all()
        self.assertEqual(self.log, ["post", "painel", "pankeka"])

    def test_the_failure_reaches_the_report(self):
        r = self._runner()
        r.add(_step("painel", self.log, fails=True))
        rendered = r.run_all().render()
        self.assertIn("painel fora do ar", rendered)
        self.assertIn("PRECISAM DE VOCÊ", rendered)

    def test_failure_names_the_exception_type_and_place(self):
        r = self._runner()
        r.add(_step("painel", self.log, fails=True))
        report = r.run_all()
        detail = [e for e in report._all if e.status is Status.FALHOU][0].detail
        self.assertIn("RuntimeError", detail)
        self.assertIn("test_runner.py:", detail)


class TestIdempotency(RunnerCase):
    def test_a_completed_step_does_not_repeat(self):
        self._runner().add(_step("post", self.log)).run_all()
        self._runner().add(_step("post", self.log)).run_all()
        self.assertEqual(self.log, ["post"])

    def test_a_failed_step_is_retried(self):
        self._runner().add(_step("painel", self.log, fails=True)).run_all()
        self._runner().add(_step("painel", self.log, fails=True)).run_all()
        self.assertEqual(self.log, ["painel", "painel"])

    def test_hourly_steps_repeat_by_design(self):
        for _ in range(3):
            self._runner().add(_step("check", self.log, once=False)).run_all()
        self.assertEqual(self.log, ["check"] * 3)

    def test_a_new_day_starts_clean(self):
        self._runner(today=date(2026, 9, 3)).add(_step("post", self.log)).run_all()
        self._runner(today=date(2026, 9, 4)).add(_step("post", self.log)).run_all()
        self.assertEqual(self.log, ["post", "post"])


class TestDryRun(RunnerCase):
    def test_dry_run_does_not_suppress_the_real_run(self):
        self._runner(dry_run=True).add(_step("post", self.log)).run_all()
        self._runner().add(_step("post", self.log)).run_all()
        self.assertEqual(self.log, ["post", "post"])

    def test_dry_run_writes_no_state_file(self):
        self._runner(dry_run=True).add(_step("post", self.log)).run_all()
        self.assertFalse(self.state_path.exists())

    def test_steps_can_see_they_are_dry(self):
        seen = []
        r = self._runner(dry_run=True)
        r.add(Step("x", "x", lambda ctx: seen.append(ctx.dry_run)))
        r.run_all()
        self.assertEqual(seen, [True])


class TestStateFile(RunnerCase):
    def test_corrupt_state_is_ignored_not_fatal(self):
        self.state_path.write_text("{not json")
        self._runner().add(_step("post", self.log)).run_all()
        self.assertEqual(self.log, ["post"])

    def test_state_records_the_day_and_the_keys(self):
        self._runner().add(_step("post", self.log)).run_all()
        stored = json.loads(self.state_path.read_text())
        self.assertEqual(stored["day"], "2026-09-03")
        self.assertEqual(stored["done"], ["post"])

    def test_missing_directory_is_created(self):
        self.state_path = Path(self.tmp.name) / "deep" / "nested" / "state.json"
        self._runner().add(_step("post", self.log)).run_all()
        self.assertTrue(self.state_path.exists())




class TestRoutineEndToEnd(RunnerCase):
    """The whole spine, with Instagram stubbed: steps assemble, run in order,
    and land in the report without any network."""

    def setUp(self):
        super().setUp()
        import os
        from unittest.mock import patch
        os.environ.update({
            "IG_ACCOUNTS": "anova.autismo,pankeka.app",
            "IG_ANOVA_AUTISMO_USER_ID": "1", "IG_ANOVA_AUTISMO_TOKEN": "t",
            "IG_PANKEKA_APP_USER_ID": "2", "IG_PANKEKA_APP_TOKEN": "t",
        })
        from .channels.instagram import Instagram
        p = patch.object(Instagram, "_request", side_effect=self._route)
        self.addCleanup(p.stop); p.start()

    def _route(self, method, path, **params):
        if method == "POST":
            return {"id": "published-1"}
        if "status_code" in params.get("fields", ""):
            return {"status_code": "FINISHED"}  # the container has fetched its media
        if path == "me/conversations":
            return {"data": []}
        if path.endswith("/media"):
            return {"data": []}
        return {}

    def _media(self, handle, folder, images=3, caption="Rotina visual"):
        d = Path(self.tmp.name) / "media" / handle / folder
        d.mkdir(parents=True)
        for i in range(1, images + 1):
            (d / f"{i}.png").write_bytes(b"x")
        if caption:
            (d / "caption.txt").write_text(caption, encoding="utf-8")
        return Path(self.tmp.name) / "media"

    def test_daily_publishes_the_days_folder_and_reports_it(self):
        from .routine import daily
        root = self._media("anova.autismo", "01-rotina-visual")
        r = self._runner()
        for step in daily(today=date(2026, 9, 3), root=str(root)):
            r.add(step)
        rendered = r.run_all().render()
        self.assertIn("Publicação realizada", rendered)
        self.assertIn("Carrossel, 3 imagens", rendered)
        self.assertIn("Rotina visual", rendered)
        self.assertIn("01-rotina-visual", rendered)

    def test_a_single_image_folder_is_not_called_a_carousel(self):
        from .routine import daily
        root = self._media("anova.autismo", "01-solo", images=1)
        r = self._runner()
        for step in daily(today=date(2026, 9, 3), root=str(root)):
            r.add(step)
        rendered = r.run_all().render()
        self.assertIn("Imagem única", rendered)

    def test_no_folders_prepared_still_runs_the_checks(self):
        from .routine import daily
        r = self._runner()
        for step in daily(today=date(2026, 9, 3), root=str(Path(self.tmp.name) / "empty")):
            r.add(step)
        rendered = r.run_all().render()
        self.assertNotIn("Publicação realizada", rendered)
        self.assertIn("Caixa de entrada vazia", rendered)

    def test_hourly_steps_are_not_once_per_day(self):
        from .routine import hourly
        self.assertTrue(all(not s.once_per_day for s in hourly()))


class TestMediaRotation(unittest.TestCase):
    """One folder a day, in order, cycling round."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for n in range(1, 4):
            d = self.root / "anova.autismo" / f"{n:02d}-post"
            d.mkdir(parents=True)
            (d / "1.png").write_bytes(b"x")
            (d / "2.png").write_bytes(b"x")
            (d / "caption.txt").write_text(f"legenda {n}", encoding="utf-8")

    def _on(self, day):
        from .media import post_for
        return post_for("anova.autismo", today=day, root=self.root)

    def test_consecutive_days_get_consecutive_folders(self):
        start = date(2026, 9, 3)
        names = [self._on(start + timedelta(days=i)).name for i in range(3)]
        self.assertEqual(len(set(names)), 3, f"expected three distinct posts, got {names}")

    def test_it_cycles_rather_than_running_out(self):
        start = date(2026, 9, 3)
        first = self._on(start).name
        self.assertEqual(self._on(start + timedelta(days=3)).name, first)

    def test_the_same_day_always_gives_the_same_post(self):
        day = date(2026, 9, 3)
        self.assertEqual(self._on(day).name, self._on(day).name)

    def test_caption_comes_from_the_file(self):
        self.assertTrue(self._on(date(2026, 9, 3)).caption.startswith("legenda "))

    def test_urls_are_public_and_ordered(self):
        post = self._on(date(2026, 9, 3))
        self.assertEqual(len(post.image_urls), 2)
        self.assertTrue(all(u.startswith("https://") for u in post.image_urls))
        self.assertTrue(post.image_urls[0].endswith("1.png"))
        self.assertTrue(post.image_urls[1].endswith("2.png"))

    def test_urls_describe_the_repo_not_this_disk(self):
        # The checkout is rarely the working directory. A URL built from the
        # local path carries "/tmp/..." into it and Instagram cannot fetch it.
        post = self._on(date(2026, 9, 3))
        for url in post.image_urls:
            self.assertNotIn(str(self.root), url)
            self.assertNotIn("/tmp/", url)
            self.assertIn(f"/media/anova.autismo/{post.name}/", url)

    def test_the_media_host_can_be_moved_without_touching_code(self):
        # Renaming the repo, or serving the images from anovasaude.org, should
        # cost one environment variable rather than an edit.
        import importlib
        import os
        from unittest.mock import patch
        with patch.dict(os.environ, {"IG_MEDIA_BASE": "https://autismo.anovasaude.org/posts"}):
            import secretary.media as media
            importlib.reload(media)
            url = media.post_for("anova.autismo", date(2026, 9, 3), root=self.root).image_urls[0]
        importlib.reload(media)
        self.assertTrue(url.startswith("https://autismo.anovasaude.org/posts/media/"))

    def test_url_has_no_double_slashes_after_the_scheme(self):
        for url in self._on(date(2026, 9, 3)).image_urls:
            self.assertNotIn("//", url.split("://", 1)[1])

    def test_a_folder_with_no_images_is_skipped(self):
        (self.root / "anova.autismo" / "99-vazia").mkdir()
        from .media import post_folders
        self.assertNotIn("99-vazia", [f.name for f in post_folders("anova.autismo", self.root)])

    def test_missing_caption_is_empty_not_an_error(self):
        d = self.root / "pankeka.app" / "01-sem-legenda"
        d.mkdir(parents=True)
        (d / "1.png").write_bytes(b"x")
        from .media import post_for
        self.assertEqual(post_for("pankeka.app", date(2026, 9, 3), root=self.root).caption, "")

    def test_account_with_no_folder_returns_nothing(self):
        from .media import post_for
        self.assertIsNone(post_for("nao.existe", date(2026, 9, 3), root=self.root))

    def test_more_than_ten_images_is_trimmed_to_the_carousel_limit(self):
        d = self.root / "pankeka.app" / "01-muitas"
        d.mkdir(parents=True)
        for i in range(1, 15):
            (d / f"{i:02d}.png").write_bytes(b"x")
        from .media import post_for
        self.assertEqual(len(post_for("pankeka.app", date(2026, 9, 3), root=self.root).image_urls), 10)


def _ago(**kw):
    from datetime import timezone
    return (datetime.now(timezone.utc) - timedelta(**kw)).isoformat().replace("+00:00", "+0000")


class TestAutoReply(RunnerCase):
    """What gets answered automatically, and what must never be."""

    THREADS = {
        "t1": {"text": "Qual a idade indicada para o teste?", "user": "mae_do_pedro", "age": {"hours": 2}},
        "t2": {"text": "não aguento mais, penso em suicídio", "user": "anon_23", "age": {"hours": 1}},
        "t3": {"text": "Vocês atendem em Niterói?", "user": "carlos", "age": {"days": 3}},
    }

    def setUp(self):
        super().setUp()
        import os
        from unittest.mock import patch
        os.environ.update({"IG_ACCOUNTS": "anova.autismo", "IG_ANOVA_AUTISMO_TOKEN": "t"})
        self.sent = []
        from .channels.instagram import Instagram
        p1 = patch.object(Instagram, "_request", side_effect=self._route)
        p2 = patch.object(Instagram, "send_message", side_effect=self._send)
        for p in (p1, p2):
            self.addCleanup(p.stop); p.start()

    def _send(self, recipient_id, text):
        self.sent.append((recipient_id, text))
        return "mid.1"

    def _route(self, method, path, **params):
        if path == "me":
            return {"id": "999999"}
        if path == "me/conversations":
            return {"data": [{"id": k} for k in self.THREADS]}
        if path in self.THREADS:
            t = self.THREADS[path]
            return {"messages": {"data": [{"id": "m", "created_time": _ago(**t["age"]),
                                           "message": t["text"],
                                           "from": {"id": path, "username": t["user"]}}]}}
        if path.endswith("/media"):
            return {"data": []}
        return {}

    def _run(self, dry_run=False):
        from .routine import instagram_messages
        r = self._runner(dry_run=dry_run)
        r.add(instagram_messages("anova.autismo"))
        return r.run_all().render()

    def test_an_ordinary_question_is_answered(self):
        self._run()
        self.assertEqual([r for r, _ in self.sent], ["t1"])

    def test_a_message_about_self_harm_is_never_answered_automatically(self):
        rendered = self._run()
        self.assertNotIn("t2", [r for r, _ in self.sent])
        self.assertIn("para você responder", rendered)
        self.assertIn("anon_23", rendered)

    def test_the_reply_points_at_the_screening_without_diagnosing(self):
        self._run()
        body = self.sent[0][1]
        self.assertIn("link do perfil", body)
        self.assertIn("não é diagnóstico", body)

    def test_outside_the_window_is_never_even_attempted(self):
        self._run()
        self.assertNotIn("t3", [r for r, _ in self.sent])

    def test_dry_run_sends_nothing(self):
        # Deliberately does NOT use the send_message stub: the dry-run guard
        # lives inside it, so stubbing it out would test the mock rather than
        # the code. Let the real method run and watch the wire instead.
        from unittest.mock import patch

        from .channels.instagram import Instagram
        with patch.object(Instagram, "send_message", Instagram.send_message), \
                patch("requests.Session.post") as post:
            self._run(dry_run=True)
        post.assert_not_called()

    def test_one_failing_send_does_not_stop_the_others(self):
        from unittest.mock import patch
        calls = []

        def flaky(recipient_id, text):
            calls.append(recipient_id)
            raise RuntimeError("rate limited")

        with patch("secretary.channels.instagram.Instagram.send_message", side_effect=flaky):
            rendered = self._run()
        self.assertIn("falhou ao enviar", rendered)
        self.assertIn("PRECISAM DE VOCÊ", rendered)

    def test_the_report_says_what_was_answered(self):
        rendered = self._run()
        self.assertIn("1 mensagem respondida", rendered)
        self.assertIn("mae_do_pedro", rendered)


if __name__ == "__main__":
    unittest.main(verbosity=2)
