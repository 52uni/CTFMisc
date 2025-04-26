@ECHO OFF
ECHO Set WshShell = Wscript.CreateObject("Wscript.Shell") >%temp%\tmp.vbs
ECHO pt = "%AppData%\Microsoft\Windows\SendTo" >>%temp%\tmp.vbs
CMD /c "ECHO ^Set MyLink = WshShell.CreateShortcut(pt ^& "\使用Foremost分解.lnk")" >>%temp%\tmp.vbs"
ECHO MyLink.TargetPath = "%~dp0Run.cmd" >>%temp%\tmp.vbs
ECHO MyLink.WorkingDirectory = "%~dp0" >>%temp%\tmp.vbs
ECHO MyLink.Save >>%temp%\tmp.vbs
cscript /nologo %temp%\tmp.vbs
echo 添加成功！在目标文件上右键-发送到-使用Foremost分解即可
pause