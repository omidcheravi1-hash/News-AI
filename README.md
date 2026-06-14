# خبرنامه روزانه هوش مصنوعی 🤖

ارسال خودکار اخبار ۲۴ ساعته هوش مصنوعی به تلگرام — هر روز ساعت ۸ صبح به وقت تهران، به زبان فارسی، مرتب‌شده بر اساس اهمیت.

## جریان کار

```
RSS Feeds (11 منبع) → Claude (ترجمه + رتبه‌بندی) → Telegram Bot
```

منابع: TechCrunch · VentureBeat · MIT Technology Review · The Verge · Wired · AI News · Hugging Face · Google AI Blog · OpenAI Blog · DeepMind · The New Stack

---

## راه‌اندازی

### ۱. ساخت ربات تلگرام

1. در تلگرام به **@BotFather** پیام دهید و `/newbot` را اجرا کنید
2. یک نام و username برای ربات انتخاب کنید
3. **Bot Token** را که BotFather می‌دهد کپی کنید

### ۲. گرفتن Chat ID

1. ربات را در تلگرام پیدا کرده و `/start` بزنید
2. در مرورگر آدرس زیر را باز کنید (توکن ربات را جایگزین کنید):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
3. در پاسخ JSON، مقدار `chat.id` را بیابید — این **Chat ID** شماست

> اگر می‌خواهید اخبار در یک گروه یا کانال دریافت شود، ربات را به آن اضافه کرده و به‌عنوان Admin تنظیم کنید، سپس Chat ID گروه/کانال را استفاده کنید.

### ۳. تنظیم Secrets در GitHub

در مخزن GitHub → **Settings → Secrets and variables → Actions → New repository secret** سه متغیر زیر را اضافه کنید:

| نام Secret | مقدار |
|---|---|
| `OPENAI_API_KEY` | کلید API از [platform.openai.com](https://platform.openai.com) |
| `TELEGRAM_BOT_TOKEN` | توکن ربات از BotFather |
| `TELEGRAM_CHAT_ID` | شناسه چت یا گروه/کانال |

### ۴. فعال‌سازی GitHub Actions

پس از push کردن کد، به تب **Actions** در GitHub بروید و در صورت نیاز Actions را فعال کنید.

---

## تست دستی

از تب **Actions** روی **Daily AI News Digest** کلیک کرده و **Run workflow** را بزنید. گزینه `force_send` را فعال بگذارید تا بدون نیاز به ساعت ۸ صبح ارسال شود.

---

## زمانبندی

- GitHub Actions دو بار در روز اجرا می‌شود (ساعت ۳:۳۰ و ۴:۳۰ UTC)
- اسکریپت Python بررسی می‌کند آیا ساعت تهران در بازه ۷:۴۵–۸:۳۰ صبح است
- این رویکرد هم زمستان (IRST = UTC+3:30) و هم تابستان (IRDT = UTC+4:30) را پوشش می‌دهد

---

## ساختار پروژه

```
News-AI/
├── main.py                        # نقطه ورود اصلی
├── requirements.txt
├── src/
│   ├── news_fetcher.py            # دریافت اخبار از RSS
│   ├── news_processor.py          # پردازش و ترجمه با Claude
│   └── telegram_sender.py         # ارسال به تلگرام
└── .github/workflows/
    └── daily_news.yml             # زمانبندی خودکار
```
