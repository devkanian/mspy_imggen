@echo off
set /P venv_name=Give me venv name:
echo %venv_name%>>venv_name.txt
cd ..
python -m venv %venv_name%
cmd /k 