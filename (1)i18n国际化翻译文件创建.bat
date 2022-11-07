@echo off
rem 该文件必用ANSI编码
rem Python安装路径
for /f "delims=" %%a in ('where python ^| findstr "Python"') do (set PYTHON_PATH=%%a%~dp1)
call :extract %PYTHON_PATH%
rem 根目录路径
set ROOT=%cd%
rem 源文件目录相对路径
set SRC=src
call :i18ncreate
pause
goto:End

:extract
rem 获取到文件路径
set PYTHON_PATH=%~dp1
goto:eof

:i18ncreate
	rem 开启延迟变量
	@setlocal enableextensions enabledelayedexpansion
	echo ===============国际化翻译文件创建===============
	set file_need_i18n=
	echo ====扫描源目录下的所有.py文件====
	for /r %ROOT%\%SRC%\ %%i in (*.py) do (
		findstr /i /c:"frame.internation" "%%i" >nul 2>nul && set file_need_i18n=!file_need_i18n! %%i || set t=
	)
	echo %file_need_i18n%
	echo ====po文件创建====
	set curdir=%ROOT%\i18n
	for /f %%i in ('dir /b /ad "%curdir%"') do (
		echo %curdir%\%%i\LC_MESSAGES\resource.po
		python %PYTHON_PATH%\Tools\i18n\pygettext.py -o %curdir%\%%i\LC_MESSAGES\resource.po %file_need_i18n%
	)
goto:eof

:End