@echo off
where python
if %ERRORLEVEL% geq 1 goto not_found_python
python ai-helper.py
pause
exit /b 0

:not_found_python
echo Pythonが見つかりません。
pause
exit /b 1
