::@echo off
title Cno Foremost
color 3f
echo %1 >path.txt
echo %~dp0>cdir.txt
set /p cdir=<cdir.txt
find "%cdir%" path.txt
echo %errorlevel%
if %errorlevel%==0 goto fail

:ctn
del /s /q output\*
rd /s /q output
cls
echo ���ڴ���Ŀ���ļ������Ժ�
start /wait Foremost.exe "%1"
explorer output
exit

:fail
title ���޾���
cls
echo.
echo.
echo                        ��⵽���޷ֽ⣬Ϊ�˱������������������Զ���ͣ����Ϊ
echo       ��������������򽫻��Ŀ���ļ��ƶ���Foremostͬ��Ŀ¼����ɾ�����������ļ����н�һ���ֽ�
echo        �����Ҫͬʱ�������������ļ�����رմ˴��ڣ�����Ҫ�������ļ��ƶ�������Ŀ¼�����·ֽ�
echo.
echo.
echo.
pause
set /p target=<path.txt
for /f "delims=" %%i in ("%target:"=%") do set name=%%~nxi
echo %name%
move "%1" "%~dp0"
del /s /q output\*
rd /s /q output
cls
echo ���ڴ���Ŀ���ļ������Ժ�
cd /d "%~dp0"
start /wait Foremost.exe "%name%"
explorer output
exit