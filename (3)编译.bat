@echo off
rem 该文件必用ANSI编码
rem Python安装路径
for /f "delims=" %%a in ('where python ^| findstr "Python"') do (set PYTHON_PATH=%%a%~dp1)
call :extract %PYTHON_PATH%
rem 项目名称
pushd %1 & for %%i in (.) do set PROJECT_NAME=%%~ni
rem 根目录路径
set ROOT=%cd%
rem 使用默认的nuitka
set NUITKA=nuitka
rem 输出目录相对路径
set OUTPUT=output
rem 图标相对路径
set ICO=res\template.ico
rem 源文件目录相对路径
set SRC=src
rem 源文件目录下 主文件名称
set MAIN=%PROJECT_NAME%
rem 国际化翻译文件编译
call :i18ncompile
rem 编译
call :begincompile
rem 创建快捷方式
call :createlnk
echo ====================结束====================
pause
goto:End

:extract
rem 获取到文件路径
set PYTHON_PATH=%~dp1
goto:eof

:begincompile
	echo ====================编译====================
	rem 参数，使用已安装的gcc
	set FLAG=--mingw64 --standalone --nofollow-imports
	rem --show-progress --show-memory 
	call %NUITKA% %FLAG% --output-dir=%OUTPUT% --windows-icon-from-ico=%ICO% --follow-import-to=%SRC% %SRC%\%MAIN%.py
goto:eof

:createlnk
	echo ===============创建的快捷方式===============
	set workingDir=%~dp0\%OUTPUT%\%MAIN%.dist
	set targetPath=%workingDir%\%MAIN%.exe
	set lnkPath=%~dp0\%MAIN%.lnk
	set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
	echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
	echo sLinkFile = "%lnkPath%" >> %SCRIPT%
	echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
	::设置快捷方式的目标位置
	echo oLink.TargetPath = "%targetPath%" >> %SCRIPT%
	::设置快捷方式的起始位置
	echo oLink.WorkingDirectory = "%workingDir%" >> %SCRIPT%
	echo oLink.Save >> %SCRIPT%
	cscript /nologo %SCRIPT%
	del %SCRIPT%
	echo 生成快捷方式%lnkPath%
goto:eof

:i18ncompile
	echo ===============国际化翻译文件编译===============
	set curdir=%ROOT%\i18n
	for /f %%i in ('dir /b /ad "%curdir%"') do (
		python %PYTHON_PATH%\Tools\i18n\msgfmt.py -o %curdir%\%%i\LC_MESSAGES\resource.mo %curdir%\%%i\LC_MESSAGES\resource.po
	)
goto:eof

:movebin
	move %OUTPUT%\%MAIN%.dist\%MAIN%.exe .\
goto:eof

:End