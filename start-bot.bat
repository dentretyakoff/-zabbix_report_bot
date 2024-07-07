@echo off

rem Установите полный путь к исполняемому файлу Python в виртуальном окружении
set VIRTUAL_ENV=".\venv"

rem Установите полный путь к скрипту Python, который вы хотите запустить
set SCRIPT=".\zabbix-report-bot.py"

rem Активируйте виртуальное окружение
call %VIRTUAL_ENV%\Scripts\activate.bat

rem Запустите скрипт Python
python %SCRIPT%

rem Деактивируйте виртуальное окружение (опционально)
call %VIRTUAL_ENV%\Scripts\deactivate.bat