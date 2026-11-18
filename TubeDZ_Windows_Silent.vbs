' ========================================================
' TubeDZ 🇩🇿 — Windows Silent Desktop Launcher
' Lance TubeDZ directement sans fenêtre de commande noire
' ========================================================

On Error Resume Next
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
batFile = fso.BuildPath(scriptDir, "TubeDZ_Windows_Portable.bat")

If fso.FileExists(batFile) Then
    Set WshShell = CreateObject("WScript.Shell")
    ' Mode 0 = fenêtre totalement invisible, False = ne bloque pas le script
    WshShell.Run Chr(34) & batFile & Chr(34), 0, False
    Set WshShell = Nothing
Else
    ' Fallback direct si le .bat est introuvable
    Set WshShell = CreateObject("WScript.Shell")
    WshShell.Run "https://rr3050026-pixel.github.io/TubeDZ/", 1, False
    Set WshShell = Nothing
End If

Set fso = Nothing
