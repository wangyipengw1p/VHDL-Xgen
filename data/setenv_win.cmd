@echo off
set CURRENTFOLDER=%cd%
cd %~dp0
cd ..
set VHDLXGEN_PATH=%cd%
set vxgen=python %VHDLXGEN_PATH%\src\vxgen.py
cd %CURRENTFOLDER%
