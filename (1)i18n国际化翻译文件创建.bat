@echo off
rem ���ļ�����ANSI����
rem Python��װ·��
for /f "delims=" %%a in ('where python ^| findstr "Python"') do (set PYTHON_PATH=%%a%~dp1)
call :extract %PYTHON_PATH%
rem ��Ŀ¼·��
set ROOT=%cd%
rem Դ�ļ�Ŀ¼���·��
set SRC=src
call :i18ncreate
pause
goto:End

:extract
rem ��ȡ���ļ�·��
set PYTHON_PATH=%~dp1
goto:eof

:i18ncreate
	rem �����ӳٱ���
	@setlocal enableextensions enabledelayedexpansion
	echo ===============���ʻ������ļ�����===============
	set file_need_i18n=
	echo ====ɨ��ԴĿ¼�µ�����.py�ļ�====
	for /r %ROOT%\%SRC%\ %%i in (*.py) do (
		findstr /i /c:"frame.internation" "%%i" >nul 2>nul && set file_need_i18n=!file_need_i18n! %%i || set t=
	)
	echo %file_need_i18n%
	echo ====po�ļ�����====
	set curdir=%ROOT%\i18n
	for /f %%i in ('dir /b /ad "%curdir%"') do (
		echo %curdir%\%%i\LC_MESSAGES\resource.po
		python %PYTHON_PATH%\Tools\i18n\pygettext.py -o %curdir%\%%i\LC_MESSAGES\resource.po %file_need_i18n%
	)
goto:eof

:End