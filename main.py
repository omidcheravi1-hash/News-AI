import os
import sys
from datetime import datetime

import pytz


def _is_tehran_send_window() -> bool:
    """Return True if Tehran clock is in the 07:45–08:30 window."""
    tehran = pytz.timezone("Asia/Tehran")
    now = datetime.now(tehran)
    minutes = now.hour * 60 + now.minute
    return (7 * 60 + 45) <= minutes <= (8 * 60 + 30)


def main() -> None:
    event = os.environ.get("GITHUB_EVENT_NAME", "manual")
    force = os.environ.get("FORCE_SEND", "false").lower() == "true"

    # When triggered on a schedule, only proceed inside the send window.
    # workflow_dispatch always proceeds so users can test on demand.
    if event == "schedule" and not force:
        if not _is_tehran_send_window():
            tehran = pytz.timezone("Asia/Tehran")
            now = datetime.now(tehran)
            print(f"Outside send window (Tehran: {now.strftime('%H:%M')}). Skipping.")
            sys.exit(0)

    from src.news_fetcher import fetch_all_news
    from src.news_processor import process_news
    from src.telegram_sender import send_daily_digest

    print("── Step 1: Fetching AI news from the last 24 hours ──")
    articles = fetch_all_news()
    print(f"Total unique articles: {len(articles)}")

    if not articles:
        print("No articles found. Exiting.")
        sys.exit(0)

    print("\n── Step 2: Processing & translating with Claude ──")
    processed = process_news(articles)
    print(f"Selected top {len(processed)} articles")

    if not processed:
        print("No articles after processing. Exiting.")
        sys.exit(0)

    print("\n── Step 3: Sending to Telegram ──")
    send_daily_digest(processed)
    print("\n✓ Daily AI news digest sent successfully!")


if __name__ == "__main__":
    main()
