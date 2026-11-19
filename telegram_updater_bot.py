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

def get_discovered_chats(token):
    res = api_call(token, "getUpdates")
    chats = {}
    if res.get("ok"):
        for update in res.get("result", []):
            msg = update.get("message") or update.get("channel_post") or update.get("my_chat_member", {}).get("chat")
            if isinstance(msg, dict):
                chat = msg.get("chat") if "chat" in msg else msg
                if chat and "id" in chat:
                    cid = chat["id"]
                    title = chat.get("title") or chat.get("username") or chat.get("first_name") or str(cid)
                    ctype = chat.get("type", "unknown")
                    chats[cid] = {"title": title, "type": ctype}
    return chats

def send_message(token, chat_id, text):
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    return api_call(token, "sendMessage", data)

def broadcast(token):
    chats = get_discovered_chats(token)
    if not chats:
        print("No chats found yet. Make sure the bot is added to the group and a message was sent.")
        return False
    v = load_version()
    msg = format_update_message(v)
    for cid, cinfo in chats.items():
        print(f"Sending update to {cinfo['title']} ({cid})...")
        res = send_message(token, cid, msg)
        print("Result:", res)
    return True

if __name__ == "__main__":
    token = os.environ.get("TELEGRAM_BOT_TOKEN", DEFAULT_BOT_TOKEN)
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"

    if cmd == "check":
        info = api_call(token, "getMe")
        print("Bot Info:", json.dumps(info, indent=2, ensure_ascii=False))
        chats = get_discovered_chats(token)
        print("Discovered Chats:", json.dumps(chats, indent=2, ensure_ascii=False))
    elif cmd == "broadcast":
        broadcast(token)
    elif cmd == "send":
        cid = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("TELEGRAM_CHAT_ID")
        if not cid:
            print("Usage: python3 telegram_updater_bot.py send <CHAT_ID>")
            sys.exit(1)
        v = load_version()
        res = send_message(token, cid, format_update_message(v))
        print("Sent:", res)
