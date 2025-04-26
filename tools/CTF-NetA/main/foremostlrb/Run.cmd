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
echo 正在处理目标文件，请稍候
start /wait Foremost.exe "%1"
explorer output
exit

:fail
title 套娃警告
cls
echo.
echo.
echo                        检测到套娃分解，为了保护数据完整程序已自动暂停此行为
echo       按下任意键，程序将会把目标文件移动至Foremost同级目录，并删除其余生成文件进行进一步分解
echo        如果需要同时保留其他生成文件，请关闭此窗口，将需要保留的文件移动至其他目录后重新分解
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
echo 正在处理目标文件，请稍候
cd /d "%~dp0"
start /wait Foremost.exe "%name%"
explorer output
exit