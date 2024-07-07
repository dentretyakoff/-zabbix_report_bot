# Телеграм-бот для ежедневных отчетов

Простой телеграм-бот, который отправляет ежедневные отчеты в чат или канал Telegram.
Также бот отвечает на команды: `/start`, `/report`, `/vpn`.
Используемые библиотеки:
- python-telegram-bot==13.7 - отправка сообщений, обработка команд,
- Pillow==9.5.0 - формирование отчета,
- paramiko==3.2.0 - получение данных от mikrotik,
- pyzabbix==1.3.0 - получение данных от zabbix.

## Установка и настройка

- Клонируйте репозиторий: `git clone git@github.com:dentretyakoff/zabbix_report_bot.git`
- Перейдите в директорию проекта: `cd ваш-репозиторий`
- Создайте и активируйте виртуальное окружение: `python3 -m venv venv`
- Установите зависимости: `pip install -r requirements.txt`
- Создайте файл .env и запишите в него необходимые переменные окружения:
    - `TELEGRAM_TOKEN` - токен бота
    - `TELEGRAM_CHAT_ID` - id чата или группы
    - `ZABBIX_USER` - пользователь zabbix для api
    - `ZABBIX_PASSWORD` - пароль пользователя zabbix
    - `ZABBIX_SERVER` - адрес сервера zabbix
    - `MIKROTIK_USER` - пользователь mikrotik
    - `MIKROTIK_PASSWORD` - пароль mikrotik
    - `MIKROTIK_HOSTNAME` - адрес mikrotik
- Заполните параметры в кофиг файле `./configs/base.py`:
    - `PROXY_URL` - адрес прокси если необходим или оставить пустым `''`
    - `TIMEZONE` - часовой пояс для заданий по расписанию


## Использование

- Запустите приложение: python zabbix-report-bot.py
- В Windows для запуска можно использовать start-bot.bat
- Настройте запуск с помощью планировщика задач Windows или cron Linux при старте компьютера.
- Бот будет автоматически отправлять ежедневные отчеты в настроенный чат или канал Telegram.
- Бот отвечает на команды:
    - `/start` - начать диалог
    - `/report` - получить отчет по текущим проблемам
    - `/vpn` - список активных подключений vpn

## Лицензия

[MIT License](https://opensource.org/licenses/MIT)