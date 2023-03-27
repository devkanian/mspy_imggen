@echo off
SET venvname_file=venv_name.txt
if exist %venvname_file% (
set /p venv_name=<%venvname_file% 
) else (
echo "%venvname_file%" does not exist & GOTO:end
)
echo venv name is: %venv_name%
cd..
CALL %venv_name%\Scripts\activate
python -m pip install --upgrade pip
cmd /k 
exit 0

:end
cmd /k 
