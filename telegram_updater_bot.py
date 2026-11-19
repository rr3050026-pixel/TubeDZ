#!/usr/bin/env python3
"""
Telegram Auto-Updater Bot for TubeDZ & DZ Music Pro (« وزارة المساكين »)
Author: Antigravity Assistant & TubeDZ Team
"""

import os
import sys
import json
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
    return {}

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

def format_tubedz_message():
    msg = f"🔔 *تحديث جديد متاح رسمياً | « وزارة المساكين »* 🇩🇿\n\n"
    msg += f"🚀 *الإصدار الرسمي:* Tube DZ v1.0.0\n"
    msg += f"📅 *تاريخ الإطلاق:* 2026-11-19\n\n"
    msg += f"📝 *أبرز ميزات هذا الإصدار:*\n"
    msg += f"الإصدار الرسمي الأول لتطبيق Tube DZ بدون إعلانات مع دعم التشغيل في الخلفية وجودة 4K وتوفير باقة الإنترنت.\n\n"
    msg += f"📥 *روابط التحميل المباشرة:*\n"
    msg += f"• [تحميل تطبيق Tube DZ للأندرويد (APK)](https://github.com/rr3050026-pixel/TubeDZ/releases/download/v1.0.0/TubeDZ.apk)\n"
    msg += f"• [سيرفر بديل سريع Tube DZ على VexFile](https://vexfile.com/download/czYlJWeyxv)\n"
    msg += f"• [تحميل تطبيق MicroG لتسجيل Google (APK)](https://github.com/rr3050026-pixel/TubeDZ/releases/download/v1.0.0/microg.apk)\n"
    msg += f"• [تحميل نسخة الكمبيوتر TubeDZ PC (ZIP)](https://github.com/rr3050026-pixel/TubeDZ/raw/main/TubeDZ-PC-Portable.zip)\n\n"
    msg += f"🌐 *الموقع الرسمي للمشروع:* https://rr3050026-pixel.github.io/TubeDZ/\n\n"
    msg += f"✨ _مشروع مجاني مدى الحياة بدون إعلانات برعاية وزارة المساكين للأبد._"
    return msg

def format_dzmusic_message():
    msg = f"🎵 *إطلاق رسمي وحصري | تطبيق DZ Music Pro 🇩🇿* 🎵\n"
    msg += f"« *وزارة المساكين* » تُهديكم التجربة الصوتية الأقوى لعام 2026\n\n"
    msg += f"يسر مشروع «وزارة المساكين» أن يعلن عن الإطلاق الرسمي لتطبيق *DZ Music Pro* المخصص لعشاق الموسيقى والبودكاست بأعلى جودة صوتية وبدون أي اشتراكات:\n\n"
    msg += f"🌟 *أبرز ميزات DZ Music Pro:*\n"
    msg += f"🎧 *صوت نقي Hi-Fi 320kbps:* استمع لأغانيك المفضلة بنقاء استوديو فائق.\n"
    msg += f"🚫 *خالي 100% من الإعلانات:* لا فواصل صوتية ولا بنرات مزعجة.\n"
    msg += f"🔋 *توفير باقة 4G والبطارية:* استهلاك خفيف جداً للإنترنت (تحميل الصوت فقط دون الفيديو).\n"
    msg += f"📱 *تشغيل كامل والشاشة مقفلة:* استمر بالاستماع أثناء تصفح التطبيقات أو قفل الشاشة.\n"
    msg += f"🚗 *دعم وضع السيارة (Car Audio Mode):* تجربة استماع آمنة ومريحة أثناء القيادة.\n"
    msg += f"📦 *حجم خفيف:* 86 ميغابايت فقط مع استجابة فائقة السرعة.\n\n"
    msg += f"🌐 *روابط المشروع الرسمية:*\n"
    msg += f"• [الموقع التعريفي الرسمي لـ DZ Music Pro](https://rr3050026-pixel.github.io/DZ-Music-Pro/)\n"
    msg += f"• [البوابة العالمية لمشروع وزارة المساكين](https://rr3050026-pixel.github.io/TubeDZ/)\n\n"
    msg += f"📥 *روابط التحميل المباشرة:*\n"
    msg += f"• [تحميل تطبيق DZ Music Pro (APK عبر VexFile)](https://vexfile.com/download/gTyjI2qrJm)\n"
    msg += f"• [طلب وتحميل الملف مباشرة في مجموعة التليغرام](https://t.me/+gsz8OJK-yh85ZWU0)\n\n"
    msg += f"✨ _مجاني 100% لأبناء الجزائر وعموم الشعب الجزائري._"
    return msg

def register_bot_commands(token=DEFAULT_BOT_TOKEN):
    commands = [
        {"command": "update", "description": "تحديثات وتحميل تطبيق TubeDZ 4K"},
        {"command": "dzmusic", "description": "إطلاق وتحميل تطبيق DZ Music Pro"},
        {"command": "download", "description": "جميع روابط التحميل المباشرة"},
        {"command": "website", "description": "زيارة الموقع الرسمي لوزارة المساكين"},
        {"command": "help", "description": "شرح التثبيت والمساعدة"}
    ]
    return api_call(token, "setMyCommands", {"commands": commands})

def send_message(token, chat_id, text, pin=False):
    data = {
        "chat_id": chat_id,
        "text": text,
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
    cmd = sys.argv[1] if len(sys.argv) > 1 else "dzmusic"

    if cmd == "dzmusic":
        print("Registering bot commands...")
        register_bot_commands(token)
        print("Broadcasting DZ Music Pro announcement...")
        res = send_message(token, chat_id, format_dzmusic_message(), pin=True)
        print("Result:", res)
    elif cmd == "tubedz":
        res = send_message(token, chat_id, format_tubedz_message(), pin=False)
        print("Result:", res)
    elif cmd == "check":
        print("Bot info:", api_call(token, "getMe"))
