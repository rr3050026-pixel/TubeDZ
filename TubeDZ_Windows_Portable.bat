@echo off
title TubeDZ Desktop Launcher 🇩🇿
chcp 65001 >nul

:: ========================================================
:: TubeDZ 🇩🇿 — PC Desktop Portable Launcher for Windows
:: ========================================================

set "TARGET_URL=https://rr3050026-pixel.github.io/TubeDZ/"
set "DATA_DIR=%LOCALAPPDATA%\TubeDZ_PC_Data"

:: 1. Detect modern Chromium engine (Edge is pre-installed on 100% of Windows 10/11)
set "BROWSER_EXE="

if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
    set "BROWSER_EXE=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
) else if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" (
    set "BROWSER_EXE=%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
) else if exist "%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe" (
    set "BROWSER_EXE=%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"
) else if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    set "BROWSER_EXE=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
) else if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
    set "BROWSER_EXE=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
) else if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    set "BROWSER_EXE=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
) else if exist "%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe" (
    set "BROWSER_EXE=%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe"
) else if exist "%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe" (
    set "BROWSER_EXE=%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"
)

:: 2. Launch in Dedicated Native Window (Standalone Desktop App Mode)
if not "%BROWSER_EXE%"=="" (
    start "" "%BROWSER_EXE%" --app="%TARGET_URL%" --window-size=1280,820 --no-first-run --no-default-browser-check
    exit /b 0
)

:: 3. Universal Fallback: Open in default system browser
start "" "%TARGET_URL%"
exit /b 0
