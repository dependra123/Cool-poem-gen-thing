@REM make a bat file that install all the python packages

@echo off


:start
cls

set python_ver=310


python -m pip install --upgrade pip
pip install spacy
pip install numpy
pip install pandas
pip install matplotlib
pip install bs4
python -m spacy download en_core_web_lg


pause
exit