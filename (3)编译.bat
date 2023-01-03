@echo off
rem ���ļ�����ANSI����
rem Python��װ·��
for /f "delims=" %%a in ('where python ^| findstr "Python"') do (set PYTHON_PATH=%%a%~dp1)
call :extract %PYTHON_PATH%
rem ��Ŀ����
pushd %1 & for %%i in (.) do set PROJECT_NAME=%%~ni
rem ��Ŀ¼·��
set ROOT=%cd%
rem ʹ��Ĭ�ϵ�nuitka
set NUITKA=nuitka
rem ���Ŀ¼���·��
set OUTPUT=output
rem ͼ�����·��
set ICO=res\template.ico
rem Դ�ļ�Ŀ¼���·��
set SRC=src
rem Դ�ļ�Ŀ¼�� ���ļ�����
set MAIN=%PROJECT_NAME%
rem ���ʻ������ļ�����
call :i18ncompile
rem ����
call :begincompile
rem ������ݷ�ʽ
call :createlnk
echo ====================����====================
pause
goto:End

:extract
rem ��ȡ���ļ�·��
set PYTHON_PATH=%~dp1
goto:eof

:begincompile
	echo ====================����====================
	rem ������ʹ���Ѱ�װ��gcc
	set FLAG=--mingw64 --standalone --nofollow-imports
	rem --show-progress --show-memory 
	call %NUITKA% %FLAG% --output-dir=%OUTPUT% --windows-icon-from-ico=%ICO% --follow-import-to=%SRC% %SRC%\%MAIN%.py
goto:eof

:createlnk
	echo ===============�����Ŀ�ݷ�ʽ===============
	set workingDir=%~dp0\%OUTPUT%\%MAIN%.dist
	set targetPath=%workingDir%\%MAIN%.exe
	set lnkPath=%~dp0\%MAIN%.lnk
	set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
	echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
	echo sLinkFile = "%lnkPath%" >> %SCRIPT%
	echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
	::���ÿ�ݷ�ʽ��Ŀ��λ��
	echo oLink.TargetPath = "%targetPath%" >> %SCRIPT%
	::���ÿ�ݷ�ʽ����ʼλ��
	echo oLink.WorkingDirectory = "%workingDir%" >> %SCRIPT%
	echo oLink.Save >> %SCRIPT%
	cscript /nologo %SCRIPT%
	del %SCRIPT%
	echo ���ɿ�ݷ�ʽ%lnkPath%
goto:eof

:i18ncompile
	echo ===============���ʻ������ļ�����===============
	set curdir=%ROOT%\i18n
	for /f %%i in ('dir /b /ad "%curdir%"') do (
		python %PYTHON_PATH%\Tools\i18n\msgfmt.py -o %curdir%\%%i\LC_MESSAGES\resource.mo %curdir%\%%i\LC_MESSAGES\resource.po
	)
goto:eof

:movebin
	move %OUTPUT%\%MAIN%.dist\%MAIN%.exe .\
goto:eof

:End