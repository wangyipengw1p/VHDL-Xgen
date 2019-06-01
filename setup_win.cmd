@echo off
echo The following line makes "%~dp0\data\setup_win.cmd" run once whenever cmd is opend > nul
reg add "HKLM\Software\Microsoft\Command Processor" /v "AutoRun" /t REG_SZ /d "%~dp0\data\setup_win.cmd" /f
