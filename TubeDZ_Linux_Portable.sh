#!/usr/bin/env bash
# ========================================================
# TubeDZ Desktop Launcher for Linux
# مشروع « وزارة المساكين » 🇩🇿
# ========================================================

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXT_DIR="$DIR/TubeDZ_Core"
USER_DATA="$HOME/.config/TubeDZ_Profile"
TARGET_URL="https://www.youtube.com"

# Check available browser
for BROWSER in google-chrome google-chrome-stable chromium chromium-browser brave-browser microsoft-edge; do
    if command -v "$BROWSER" >/dev/null 2>&1; then
        exec "$BROWSER" \
            --app="$TARGET_URL" \
            --user-data-dir="$USER_DATA" \
            --load-extension="$EXT_DIR" \
            --window-size=1280,820 \
            --no-first-run &
        exit 0
    fi
done

# Fallback
xdg-open "$TARGET_URL"
