@ECHO OFF
ECHO Set WshShell = Wscript.CreateObject("Wscript.Shell") >%temp%\tmp.vbs
ECHO pt = "%AppData%\Microsoft\Windows\SendTo" >>%temp%\tmp.vbs
CMD /c "ECHO ^Set MyLink = WshShell.CreateShortcut(pt ^& "\ʹ��Foremost�ֽ�.lnk")" >>%temp%\tmp.vbs"
ECHO MyLink.TargetPath = "%~dp0Run.cmd" >>%temp%\tmp.vbs
ECHO MyLink.WorkingDirectory = "%~dp0" >>%temp%\tmp.vbs
ECHO MyLink.Save >>%temp%\tmp.vbs
cscript /nologo %temp%\tmp.vbs
echo ��ӳɹ�����Ŀ���ļ����Ҽ�-���͵�-ʹ��Foremost�ֽ⼴��
pause