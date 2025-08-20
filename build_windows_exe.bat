@echo off
REM Build Windows onefile exe
pip install pyinstaller
pyinstaller --onefile --noconsole app.py
echo Build complete. Executable in .\dist\
pause
