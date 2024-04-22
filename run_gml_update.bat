@echo off
REM Activate Anaconda environment
CALL C:\anaconda\Scripts\activate.bat C:\anaconda

REM Run the Python script with Anaconda Python
C:\anaconda\python.exe "%~dp0update_gml_and_qgs_paths.py" %1

@echo on