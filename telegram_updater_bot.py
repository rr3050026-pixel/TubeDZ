#!/usr/bin/env python3
"""
Telegram Auto-Updater Bot for TubeDZ (« وزارة المساكين »)
This script can:
1. Send an immediate update announcement to the Telegram group.
2. Run as a 24/7 assistant bot that replies to /update, /download, and /start commands.
"""

import os
import sys
import json
import time
import requests

VERSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'version.json')

def load_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "latestVersion": "1.0.0",
        "releaseDate": "2026-11-19",
        "releaseNotes": {"ar": "الإصدار الرسمي لتطبيقات وزارة المساكين"},
        "downloads": {
            "tubeDzApk": "https://github.com/rr3050026-pixel/TubeDZ/releases/download/v1.0.0/TubeDZ.apk",
            "microgApk": "https://github.com/rr3050026-pixel/TubeDZ/releases/download/v1.0.0/microg.apk"
        },
        "community": {
            "website": "https://rr3050026-pixel.github.io/TubeDZ/"
        }
    }

def format_update_message(v_data):
    ver = v_data.get('latestVersion', '1.0.0')
    date = v_data.get('releaseDate', '')
    notes = v_data.get('releaseNotes', {}).get('ar', '')
    apk = v_data.get('downloads', {}).get('tubeDzApk', '')
    microg = v_data.get('downloads', {}).get('microgApk', '')
    site = v_data.get('community', {}).get('website', '')

    msg = f"🔔 *تحديث جديد متاح | « وزارة المساكين »* 🇩🇿\n\n"
    msg += f"🚀 *الإصدار الحالي:* v{ver}\n"
    if date:
        msg += f"📅 *تاريخ الإطلاق:* {date}\n\n"
    msg += f"📝 *الجديد في هذا الإصدار:*\n{notes}\n\n"
    msg += f"📥 *روابط التحميل المباشرة:*\n"
    msg += f"• [تحميل تطبيق Tube DZ (APK)]({apk})\n"
    msg += f"• [تحميل تطبيق MicroG (APK)]({microg})\n\n"
    msg += f"🌐 *الموقع الرسمي والميزات:*\n{site}\n\n"
    msg += f"✨ _تطبيق مجاني 100% بدون إعلانات برعاية وزارة المساكين للأبد._"
    return msg

def send_update_to_group(bot_token, chat_id):
    v = load_version()
    msg = format_update_message(v)
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": msg,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    res = requests.post(url, json=payload, timeout=15)
    return res.json()

def run_polling_bot(bot_token):
    print("🤖 TubeDZ Telegram Bot is listening for commands...")
    offset = None
    url = f"https://api.telegram.org/bot{bot_token}/"

    while True:
        try:
            params = {"timeout": 30}
            if offset:
                params["offset"] = offset

            resp = requests.get(url + "getUpdates", params=params, timeout=35).json()
            if not resp.get("ok"):
                time.sleep(3)
                continue

            for update in resp.get("result", []):
                offset = update["update_id"] + 1
                msg = update.get("message")
                if not msg:
                    continue

                chat_id = msg.get("chat", {}).get("id")
                text = msg.get("text", "").strip()

                if text in ["/start", "/help", "/update", "/download", "تحديث", "تحميل"]:
                    v = load_version()
                    reply_text = format_update_message(v)
                    requests.post(url + "sendMessage", json={
                        "chat_id": chat_id,
                        "text": reply_text,
                        "parse_mode": "Markdown"
                    }, timeout=10)

        except Exception as e:
            print("Error in polling:", e)
            time.sleep(5)

if __name__ == "__main__":
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if len(sys.argv) > 1 and sys.argv[1] == "send":
        if not bot_token or not chat_id:
            print("Usage: TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=... python3 telegram_updater_bot.py send")
            sys.exit(1)
        result = send_update_to_group(bot_token, chat_id)
        print("Telegram API response:", result)
    else:
        if not bot_token:
            print("Please set TELEGRAM_BOT_TOKEN environment variable.")
            sys.exit(1)
        run_polling_bot(bot_token)
