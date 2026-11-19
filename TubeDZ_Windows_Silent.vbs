' ========================================================
' TubeDZ Desktop Silent Launcher (بدون نافذة أوامر سوداء)
' مشروع « وزارة المساكين » 🇩🇿
' ========================================================

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

strScriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
strBatPath = strScriptDir & "\TubeDZ_Windows_Portable.bat"

If fso.FileExists(strBatPath) Then
    ' Run hidden (0) without waiting (False)
    WshShell.Run """" & strBatPath & """", 0, False
Else
    WshShell.Run "https://www.youtube.com"
End If
