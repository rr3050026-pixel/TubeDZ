@echo off
title TubeDZ Desktop — وزارة المساكين 🇩🇿
chcp 65001 >nul

:: =========================================================================
::  TubeDZ PC Desktop Portable Edition | « وزارة المساكين » 🇩🇿
::  YouTube 100%% Ad-Free, Background Play, 4K HDR, AMOLED Theme
:: =========================================================================

set "SCRIPT_DIR=%~dp0"
set "EXTENSION_DIR=%SCRIPT_DIR%TubeDZ_Core"
set "USER_DATA=%LOCALAPPDATA%\TubeDZ_PC_Profile"
set "TARGET_URL=https://www.youtube.com"

:: 1. Search for Chromium Browser Engine (Edge is pre-installed on 100% Windows 10/11)
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

:: 2. Launch Dedicated Native Standalone Window with TubeDZ Core Engine (AdBlock & AMOLED)
if not "%BROWSER_EXE%"=="" (
    start "" "%BROWSER_EXE%" ^
        --app="%TARGET_URL%" ^
        --user-data-dir="%USER_DATA%" ^
        --load-extension="%EXTENSION_DIR%" ^
        --window-size=1280,820 ^
        --no-first-run ^
        --no-default-browser-check ^
        --autoplay-policy=no-user-gesture-required ^
        --disable-features=Translate
    exit /b 0
)

:: 3. Fallback: Launch default browser
start "" "%TARGET_URL%"
exit /b 0
