' ========================================================
' TubeDZ 🇩🇿 — Windows Silent Desktop Launcher
' Lance TubeDZ comme une véritable application native sans console noire
' ========================================================

Set WshShell = CreateObject("WScript.Shell")
strPath = WshShell.CurrentDirectory
batPath = Chr(34) & strPath & "\TubeDZ_Windows_Portable.bat" & Chr(34)
WshShell.Run batPath, 0, False
Set WshShell = Nothing
