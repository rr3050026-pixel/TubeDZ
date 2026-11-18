#!/usr/bin/env bash
# ========================================================
# TubeDZ 🇩🇿 — Linux PC Desktop Portable Launcher
# ========================================================

TARGET_URL="https://rr3050026-pixel.github.io/TubeDZ/"
DATA_DIR="${HOME}/.config/tubedz_pc_data"

# Detect installed browser
BROWSER_CMD=""
for cmd in google-chrome google-chrome-stable chromium chromium-browser brave-browser microsoft-edge; do
    if command -v "$cmd" >/dev/null 2>&1; then
        BROWSER_CMD="$cmd"
        break
    fi
done

if [ -z "$BROWSER_CMD" ]; then
    echo "Ouverture de TubeDZ..."
    xdg-open "$TARGET_URL" 2>/dev/null || sensible-browser "$TARGET_URL" 2>/dev/null || x-www-browser "$TARGET_URL" 2>/dev/null &
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
