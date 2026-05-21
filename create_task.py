#!/usr/bin/env python3
"""Simple CLI to create a reminder task through local API."""

import argparse
import json
import sys
import urllib.error
import urllib.request


DEFAULT_API = "http://localhost:5000/api/reminders"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a reminder task")
    parser.add_argument("title", help="Task title")
    parser.add_argument("--description", default="", help="Task description")
    parser.add_argument("--date", dest="remind_date", help="Date in YYYY-MM-DD")
    parser.add_argument("--time", dest="remind_time", required=True, help="Time in HH:MM")
    parser.add_argument(
        "--frequency",
        default="once",
        choices=["once", "daily", "weekly", "monthly"],
        help="Reminder frequency",
    )
    parser.add_argument(
        "--notify",
        dest="notification_types",
        nargs="+",
        default=["system"],
        choices=["system", "email", "webhook"],
        help="Notification channels",
    )
    parser.add_argument("--api", default=DEFAULT_API, help="API endpoint")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    payload = {
        "title": args.title,
        "description": args.description,
        "remind_date": args.remind_date,
        "remind_time": args.remind_time,
        "frequency": args.frequency,
        "notification_types": args.notification_types,
        "is_active": True,
    }

    req = urllib.request.Request(
        args.api,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        print(f"Failed to create task: HTTP {exc.code} {detail}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Failed to connect to API: {exc.reason}", file=sys.stderr)
        return 1

    if not body.get("success"):
        print(f"API returned error: {body}", file=sys.stderr)
        return 1

    reminder = body.get("data", {})
    print(f"✅ Created task: {reminder.get('id')} - {reminder.get('title')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
