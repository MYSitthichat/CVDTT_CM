Set WshShell = CreateObject("WScript.Shell")
' Get the directory where this VBS file is located
Dim fso, scriptPath, scriptDir
Set fso = CreateObject("Scripting.FileSystemObject")
scriptPath = WScript.ScriptFullName
scriptDir = fso.GetParentFolderName(scriptPath)

' Run App.bat from the same directory
WshShell.Run Chr(34) & scriptDir & "\App.bat" & Chr(34), 0
