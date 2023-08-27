
REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Update pip
python -m pip install --upgrade pip

REM Install wheel and setuptools
pip install wheel setuptools

REM Install the requirements
pip install -r requirements.txt

REM run the program
python copy_selected.py

echo Setup complete!
pause