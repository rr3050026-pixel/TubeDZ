@echo off
title TubeDZ Desktop Launcher
chcp 65001 >nul

:: ========================================================
:: TubeDZ 🇩🇿 — PC Desktop Portable Launcher for Windows
:: ========================================================

set "APP_URL=https://tubedz.onrender.com"
set "LOCAL_HTML=%~dp0index.html"
set "DATA_DIR=%LOCALAPPDATA%\TubeDZ_PC_Data"
set "ICON_PATH=%~dp0TubeDZ.ico"

:: Prefer online live app if reachable, otherwise fallback to local HTML
ping -n 1 8.8.8.8 >nul 2>&1
if errorlevel 1 (
    if exist "%LOCAL_HTML%" (
        set "TARGET_URL=file:///%LOCAL_HTML:\=/%"
    ) else (
        set "TARGET_URL=%APP_URL%"
    )
) else (
    set "TARGET_URL=%APP_URL%"
)

:: Find modern Chromium engine (Edge is pre-installed on 100% of Windows 10/11)
set "BROWSER_EXE="

if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
    set "BROWSER_EXE=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
) else if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" (
    set "BROWSER_EXE=%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
) else if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    set "BROWSER_EXE=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
) else if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
    set "BROWSER_EXE=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
) else if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    set "BROWSER_EXE=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
) else if exist "%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe" (
    set "BROWSER_EXE=%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe"
)

if "%BROWSER_EXE%"=="" (
    echo [ERROR] Aucun navigateur compatible trouvé. Ouverture via le navigateur par défaut...
    start "" "%TARGET_URL%"
    exit /b
)

:: Launch TubeDZ in Dedicated Native Window (Standalone Desktop App Mode)
start "" "%BROWSER_EXE%" --app="%TARGET_URL%" --window-size=1280,820 --user-data-dir="%DATA_DIR%" --disable-plugins --no-first-run --no-default-browser-check
exit
