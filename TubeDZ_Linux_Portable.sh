#!/usr/bin/env bash
# ========================================================
# TubeDZ 🇩🇿 — Linux PC Desktop Portable Launcher
# ========================================================

APP_URL="https://tubedz.onrender.com"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_HTML="file://${SCRIPT_DIR}/index.html"
DATA_DIR="${HOME}/.config/tubedz_pc_data"

# Test internet connectivity
if ping -c 1 8.8.8.8 >/dev/null 2>&1; then
    TARGET_URL="${APP_URL}"
else
    TARGET_URL="${LOCAL_HTML}"
fi

# Detect installed browser
BROWSER_CMD=""
for cmd in google-chrome google-chrome-stable chromium chromium-browser brave-browser microsoft-edge; do
    if command -v "$cmd" >/dev/null 2>&1; then
        BROWSER_CMD="$cmd"
        break
    fi
done

if [ -z "$BROWSER_CMD" ]; then
    echo "Ouverture via xdg-open..."
    xdg-open "$TARGET_URL" &
    exit 0
fi

# Launch in Native Desktop Window
"$BROWSER_CMD" \
    --app="$TARGET_URL" \
    --window-size=1280,820 \
    --user-data-dir="$DATA_DIR" \
    --no-first-run \
    --disable-plugins \
    >/dev/null 2>&1 &
exit 0
