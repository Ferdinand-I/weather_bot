# Telegram Weather Bot<img style="margin-left: 20px;" src="https://logowiki.net/uploads/logo/w/weather-ios.svg" width=48>


Приложение написано на **Python 3.7** с использованием библиотеки **requests** и **threading**

Функционал приложения:
* Получение данных от API *Яндекс.Погоды*
* Ежедневная отправка прогноза в *Telegram*
* Добавление получателей погодных обновлений путём отправки любого сообщения боту

Техническая реализация:
* Запросы к *API Яндекс.Погоды* и к *Telgram Bot API* осуществляется с помощью библиотеки **requests**
* Процесс распараллелен на два потока с помощью библиотеки threading. Один поток отвечает за регулярную отправку сообщений. Другой за апдейты пользователей бота
* **Long polling** метод опроса сервера для получения апдейтов
* Деплой на удалённый сервер осуществляется в контейнере **Docker**

Чтобы запустить проект вам понадобятся <a href="https://developer.tech.yandex.ru/services/">API-ключ</a> для доступа к данным *Яндекс.Погоды*,
<a href="https://core.telegram.org/bots#how-do-i-create-a-bot">Telegram Bot-token</a> для настройки отправки сообщений и ваш **id** аккаунта в *Telegram*

Чтобы запустить проект локально:

1. Клонируйте репозиторий себе на компьютер, находясь в директории, откуда вы хотите в будущем запускать проект (в примере испоьзуется ссылка для подключения с помощью протокола **SSH** в консоли **BASH** для **WINDOWS**)

```BASH
git clone git@github.com:Ferdinand-I/weather_bot.git
```

2. Создайте и активируйте виртуальное окружение (в примере используется утилита **venv**), перейдите в директорию проекта

```BASH
python -m venv venv
source venv/Scripts/activate
cd weather_bot
```

3. Обновите **PIP** и установите зависимости **requirements.txt**

```BASH
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Запустите проект

```BASH
python weather_bot.py
```

Приложение умеет работать с аргументами командной строки и принимает 2 аргумента:
- литера из списка **['m', 'h', 'd']** - единицы измерения частоты отправки сообщений. **'m'** - минуты, **'h'** - часы, **'d'** - дни
- число - количество единиц измерения. Т.е. какое количество заданных единиц измерения будет между итерациями

Например, запустив такой код:

```BASH
python weather_bot.py h 24
```

Приложение будет присылать вам данные о погоде каждый 24 часа с момента запуска.

Если же аргументы не получены из командной строки, то приложение автоматически настроится на отправку уведомлений раз в сутки с момент запуска.
