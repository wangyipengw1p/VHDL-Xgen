@echo off
::The following line makes "%~dp0\data\setup_win.cmd" run once whenever cmd is opend 
reg add "HKLM\Software\Microsoft\Command Processor" /v "AutoRun" /t REG_SZ /d "%~dp0data\setenv_win.cmd" /f
echo 
echo Success!
echo 
pause
