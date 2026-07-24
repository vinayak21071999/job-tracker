"""
Sends job matches to Telegram.
Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID as environment variables
(GitHub Actions secrets in production).
"""

import os
import requests

# TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
# TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

TELEGRAM_BOT_TOKEN = "7699896031:AAGMSn_i9TiAfetwLpfX6Bwa6Xa7uYZMhJ4"
TELEGRAM_CHAT_ID = "530289659"

def send_telegram_message(text: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[notifier] Telegram credentials not set - printing instead:\n" + text)
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    try:
        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[notifier] failed to send Telegram message: {e}")


def format_job_message(job: dict) -> str:
    company = job.get("company", "Unknown company")
    title = job.get("title", "Untitled role")
    location = job.get("location", "Location not specified")
    url = job.get("url", "")
    skills = job.get("matched_skills", [])

    lines = [
        f"<b>{title}</b>",
        f"{company} — {location}",
    ]
    if skills:
        lines.append("Matched: " + ", ".join(skills[:6]))
    lines.append(url)

    return "\n".join(lines)


def notify_new_jobs(jobs):
    for job in jobs:
        send_telegram_message(format_job_message(job))
