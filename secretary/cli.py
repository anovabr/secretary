"""Command line for the Instagram channel.

    python -m secretary.cli whoami
    python -m secretary.cli inbox --account anova.autismo
    python -m secretary.cli post --account pankeka.app --image https://... --caption "..."
    python -m secretary.cli reply --account anova.autismo --comment 178... --message "..."
    python -m secretary.cli refresh-tokens

Every writing command accepts --dry-run, which prints the call it would make
and sends nothing. Use it while the approval gate is still manual.
"""

from __future__ import annotations

import argparse
import sys

from .accounts import load_account, load_accounts
from .channels.instagram import Instagram, InstagramError


def _client(args, handle: str | None = None) -> Instagram:
    return Instagram(load_account(handle or args.account), dry_run=getattr(args, "dry_run", False))


def cmd_whoami(args) -> int:
    for handle, account in sorted(load_accounts().items()):
        try:
            me = Instagram(account).whoami()
            followers = me.get("followers_count", "?")
            print(f"  {handle:<20} ok  id={me['id']}  {me.get('account_type', '?')}  {followers} followers")
        except InstagramError as exc:
            print(f"  {handle:<20} FAILED  {exc}")
    return 0


def cmd_inbox(args) -> int:
    handles = [args.account] if args.account else sorted(load_accounts())
    total = 0
    for handle in handles:
        print(f"\n{handle}")
        pending = list(_client(args, handle).unanswered_comments(limit=args.limit))
        if not pending:
            print("  nothing waiting")
            continue
        for c in pending:
            total += 1
            print(f"  [{c['id']}] @{c.get('username', '?')} — {c.get('text', '').strip()}")
            print(f"      on {c.get('permalink', c['media_id'])}")
    print(f"\n{total} comment(s) awaiting a reply")
    return 0


def cmd_messages(args) -> int:
    """Direct messages waiting on a reply, flagged by whether we may still answer."""
    handles = [args.account] if args.account else sorted(load_accounts())
    for handle in handles:
        print(f"\n{handle}")
        pending = _client(args, handle).unanswered_threads()
        if not pending:
            print("  caixa de entrada vazia")
            continue
        for t in pending:
            if t["within_window"]:
                mark, note = "  ", ""
            else:
                hours = int(t["age"].total_seconds() // 3600) if t["age"] else "?"
                mark, note = " !", f"  (fora da janela — há {hours}h, exige resposta manual)"
            print(f"{mark} [{t['conversation_id']}] @{t['sender']}{note}")
            print(f"      {t['text'].strip()}")
    return 0


def cmd_send(args) -> int:
    message_id = _client(args).send_message(args.to, args.message)
    print(f"sent on {args.account}: {message_id}")
    return 0


def cmd_run(args) -> int:
    """Execute the routine and print the report."""
    from datetime import datetime

    from .report import Report
    from .routine import daily, hourly
    from .runner import DayState, Runner

    steps = hourly() if args.hourly else daily()
    runner = Runner(Report(datetime.now()), DayState(args.state), dry_run=args.dry_run)
    for step in steps:
        runner.add(step)
    print(runner.run_all().render())
    return 0


def cmd_report(args) -> int:
    from .demo_report import build

    print(build().render())
    return 0


def cmd_post(args) -> int:
    ig = _client(args)
    if args.carousel:
        media_id = ig.publish_carousel(args.carousel.split(","), args.caption)
    elif args.reel:
        media_id = ig.publish_reel(args.reel, args.caption, cover_url=args.cover)
    else:
        media_id = ig.publish_image(args.image, args.caption)
    print(f"published to {args.account}: {media_id}")
    return 0


def cmd_reply(args) -> int:
    reply_id = _client(args).reply_to_comment(args.comment, args.message)
    print(f"replied on {args.account}: {reply_id}")
    return 0


def cmd_refresh(args) -> int:
    """Refresh every token. Prints the new values for you to store; nothing is written."""
    for handle, account in sorted(load_accounts().items()):
        try:
            result = Instagram(account).refresh_token()
            days = int(result.get("expires_in", 0)) // 86400
            print(f"  {handle:<20} renewed, valid {days} more days")
            print(f"      {_env_var(handle)}={result['access_token']}")
        except InstagramError as exc:
            print(f"  {handle:<20} FAILED  {exc}")
    return 0


def _env_var(handle: str) -> str:
    from .accounts import _env_prefix

    return f"{_env_prefix(handle)}_TOKEN"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="secretary", description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="print writes instead of sending them")

    # Repeat --dry-run on the writing subcommands so it reads naturally at the end
    # of the line too. SUPPRESS keeps an unused subcommand flag from overwriting
    # the top-level one.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--dry-run", action="store_true", default=argparse.SUPPRESS,
                        help="print writes instead of sending them")

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("whoami", help="check every configured token").set_defaults(func=cmd_whoami)
    sub.add_parser("refresh-tokens", help="extend every token by 60 days").set_defaults(func=cmd_refresh)

    p_inbox = sub.add_parser("inbox", help="comments nobody has replied to")
    p_inbox.add_argument("--account")
    p_inbox.add_argument("--limit", type=int, default=10, help="how many recent posts to scan")
    p_inbox.set_defaults(func=cmd_inbox)

    p_post = sub.add_parser("post", help="publish a post", parents=[common])
    p_post.add_argument("--account", required=True)
    p_post.add_argument("--caption", default="")
    media = p_post.add_mutually_exclusive_group(required=True)
    media.add_argument("--image", help="public https URL of a single image")
    media.add_argument("--reel", help="public https URL of a video")
    media.add_argument("--carousel", help="2-10 comma-separated image URLs")
    p_post.add_argument("--cover", help="cover image URL, reels only")
    p_post.set_defaults(func=cmd_post)

    p_msgs = sub.add_parser("messages", help="direct messages awaiting a reply")
    p_msgs.add_argument("--account")
    p_msgs.set_defaults(func=cmd_messages)

    p_send = sub.add_parser("send", help="send a direct message", parents=[common])
    p_send.add_argument("--account", required=True)
    p_send.add_argument("--to", required=True, help="the sender id from `messages`")
    p_send.add_argument("--message", required=True)
    p_send.set_defaults(func=cmd_send)

    sub.add_parser("report", help="print a worked example of the daily report").set_defaults(func=cmd_report)

    p_run = sub.add_parser("run", help="execute the routine and print the report", parents=[common])
    p_run.add_argument("--hourly", action="store_true", help="the hourly check instead of the morning run")
    p_run.add_argument("--state", default=".secretary-state.json", help="where completed steps are recorded")
    p_run.set_defaults(func=cmd_run)

    p_reply = sub.add_parser("reply", help="reply to a comment", parents=[common])
    p_reply.add_argument("--account", required=True)
    p_reply.add_argument("--comment", required=True)
    p_reply.add_argument("--message", required=True)
    p_reply.set_defaults(func=cmd_reply)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (InstagramError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
