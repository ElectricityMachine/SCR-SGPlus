@ECHO OFF
echo This script will install SG+'s script dependencies and create a virtual environment for you.
echo If you have not installed Python 3.12, please exit the script and install it from https://python.org
choice /m "Have you installed Python 3.12?"
if %errorlevel% equ 1 goto confirmed
if %errorlevel% equ 2 goto request_install

:confirmed
echo Creating venv...
call python -m venv .venv
echo Installing dependencies...
.venv\Scripts\python.exe -m pip install -r requirements.txt
echo SG+ install successful. Happy signalling!
pause
exit

:request_install
echo You have indicated you have not installed Python 3.12. Please do so, then run the script again.
PAUSE