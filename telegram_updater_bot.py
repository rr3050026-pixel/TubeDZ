#!/usr/bin/env python3
"""
Telegram Auto-Updater Bot for TubeDZ (« وزارة المساكين »)
Author: Antigravity Assistant & TubeDZ Team
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import ssl

DEFAULT_BOT_TOKEN = "9059578603:AAGknoPvyCjVojv9Lc-dc7tGR4k-G6T_OeI"
DEFAULT_CHAT_ID = -1003732255699
VERSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'version.json')

ctx = ssl._create_unverified_context()

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
            "microgApk": "https://github.com/rr3050026-pixel/TubeDZ/releases/download/v1.0.0/microg.apk",
            "pcZip": "https://github.com/rr3050026-pixel/TubeDZ/raw/main/TubeDZ-PC-Portable.zip"
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
    pc = v_data.get('downloads', {}).get('pcZip', '')
    site = v_data.get('community', {}).get('website', '')

    msg = f"🔔 *تحديث جديد متاح رسمياً | « وزارة المساكين »* 🇩🇿\n\n"
    msg += f"🚀 *الإصدار الرسمي:* v{ver}\n"
    if date:
        msg += f"📅 *تاريخ الإطلاق:* {date}\n\n"
    msg += f"📝 *أبرز ميزات هذا الإصدار:*\n{notes}\n\n"
    msg += f"📥 *روابط التحميل المباشرة:*\n"
    msg += f"• [تحميل تطبيق Tube DZ للأندرويد (APK)]({apk})\n"
    msg += f"• [تحميل تطبيق MicroG لتسجيل Google (APK)]({microg})\n"
    msg += f"• [تحميل نسخة الكمبيوتر TubeDZ PC (ZIP)]({pc})\n\n"
    msg += f"🌐 *الموقع الرسمي للمشروع:* {site}\n\n"
    msg += f"✨ _مشروع مجاني مدى الحياة بدون إعلانات برعاية وزارة المساكين للأبد._"
    return msg

def api_call(token, method, data=None):
    url = f"https://api.telegram.org/bot{token}/{method}"
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"API Error ({method}):", e)
        return {"ok": False, "error": str(e)}

def send_update(token=DEFAULT_BOT_TOKEN, chat_id=DEFAULT_CHAT_ID, pin=True):
    v = load_version()
    msg = format_update_message(v)
    data = {
        "chat_id": chat_id,
        "text": msg,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    res = api_call(token, "sendMessage", data)
    if res.get("ok") and pin:
        mid = res["result"]["message_id"]
        api_call(token, "pinChatMessage", {"chat_id": chat_id, "message_id": mid})
    return res

if __name__ == "__main__":
    token = os.environ.get("TELEGRAM_BOT_TOKEN", DEFAULT_BOT_TOKEN)
    chat_id = int(os.environ.get("TELEGRAM_CHAT_ID", DEFAULT_CHAT_ID))
    cmd = sys.argv[1] if len(sys.argv) > 1 else "send"

    if cmd == "send":
        res = send_update(token, chat_id, pin=True)
        print("Update broadcast result:", res)
    elif cmd == "check":
        print("Bot info:", api_call(token, "getMe"))
