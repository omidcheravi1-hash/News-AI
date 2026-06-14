import json
import os
import re

from openai import OpenAI

MODEL = "gpt-4o"
MAX_INPUT_ARTICLES = 50
MAX_OUTPUT_ARTICLES = 10


def process_news(articles: list[dict]) -> list[dict]:
    """Rank, deduplicate, translate and summarise articles in Persian via GPT."""

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    condensed = []
    for i, a in enumerate(articles[:MAX_INPUT_ARTICLES]):
        condensed.append(
            {
                "id": i,
                "title": a["title"],
                "description": (a["description"] or "")[:300],
                "source": a["source"],
                "published": a["published"],
                "has_image": bool(a.get("image_url")),
                "has_video": bool(a.get("video_url")),
            }
        )

    articles_json = json.dumps(condensed, ensure_ascii=False, indent=2)

    prompt = f"""تو یک روزنامه‌نگار متخصص در حوزه هوش مصنوعی هستی.
لیست زیر اخبار ۲۴ ساعت گذشته دنیای هوش مصنوعی است:

{articles_json}

وظایف:
۱. خبرهای تکراری یا خیلی مشابه را حذف کن (یکی نگه‌دار).
۲. حداکثر {MAX_OUTPUT_ARTICLES} خبر مهم را بر اساس تأثیرگذاری و جذابیت انتخاب کن.
۳. برای هر خبر:
   - عنوان را به فارسی روان و دقیق ترجمه کن.
   - یک خلاصه ۲ تا ۴ جمله‌ای به فارسی بنویس که اهمیت و جزئیات کلیدی را توضیح دهد.
   - مهم‌ترین خبر، importance_rank=1 داشته باشد.

فقط یک JSON خالص (بدون markdown، بدون توضیح اضافه) برگردان:
[
  {{
    "id": <شناسه اصلی>,
    "title_fa": "<عنوان فارسی>",
    "summary_fa": "<خلاصه فارسی>",
    "importance_rank": <عدد از ۱ به بالا>
  }}
]"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "تو یک روزنامه‌نگار متخصص هوش مصنوعی هستی که اخبار را به فارسی روان ترجمه و خلاصه می‌کنی.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=4096,
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    processed: list[dict] = json.loads(raw)

    article_map = {i: a for i, a in enumerate(articles[:MAX_INPUT_ARTICLES])}
    result = []
    for item in sorted(processed, key=lambda x: x["importance_rank"]):
        orig = article_map.get(item["id"])
        if not orig:
            continue
        result.append(
            {
                "title_fa": item["title_fa"],
                "summary_fa": item["summary_fa"],
                "importance_rank": item["importance_rank"],
                "title_en": orig["title"],
                "source": orig["source"],
                "url": orig["url"],
                "published": orig["published"],
                "image_url": orig.get("image_url", ""),
                "video_url": orig.get("video_url", ""),
            }
        )

    return result
