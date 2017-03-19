@echo off
@echo ==============================================
@echo  !! ADD PATH of your driver to PATH variable
@echo  - see the codes of run.bat
@echo ==============================================
set PATH=%PATH%;c:\Program Files\WebDrivers\
cd src
python mfdsapi.py
cd ..
