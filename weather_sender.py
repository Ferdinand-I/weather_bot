import os
import sys
import threading
import time
from datetime import datetime

import requests
import schedule
from dotenv import load_dotenv
from googletrans import Translator

load_dotenv()

RECIPIENTS_IDS = [os.getenv('TG_ID'), ]

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')

TG_GET_UPDATES = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/getUpdates'
TG_SEND_MESSAGE = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage'
YANDEX_WEATHER_API = 'https://api.weather.yandex.ru/v2/forecast?'

ICON_TEMPLATE = 'https://yastatic.net/weather/i/icons/funky/dark/{}.svg'

VALID_ARGS_MEASURE = ['h', 'd', 'm']

PREC_TYPE = {
    0: 'Без осадков',
    1: 'Дождь',
    2: 'Дождь со снегом',
    3: 'Снег',
    4: 'Град'
}

translator = Translator()


def get_userid_by_updates():
    while True:
        response = requests.get(TG_GET_UPDATES)
        result = (response.json().get('result'))
        users = [i.get('message').get('from').get('id') for i in result]
        if users:
            for i in users:
                if str(i) not in RECIPIENTS_IDS:
                    RECIPIENTS_IDS.append(str(i))
        users.clear()
        time.sleep(30)


def get_weather_data():
    """"""
    headers = {
        'X-Yandex-API-Key': YANDEX_API_KEY,
        'lat': '59.93428',
        'lon': '30.3351',
        'lang': 'ru_RU',
        'limit': '1',
        'hours': 'true',
        'extra': 'true'
    }
    response = requests.get(
        url=YANDEX_WEATHER_API,
        headers=headers
    )
    if response.status_code == 403:
        return (
            'Не удалось получить данные о погоде, так как доступ к ресурсу'
            'ограничен. Проверьте валидность вашего ключа APi.'
        )
    unix_datetime = int(response.json().get('now'))
    date_time = datetime.utcfromtimestamp(unix_datetime).strftime(
        '%A %d.%m.%y'
    )
    translate_date = translator.translate(date_time, src='en', dest='ru')
    temperature = response.json().get('fact').get('temp')
    feels_like = response.json().get('fact').get('feels_like')
    condition = translator.translate(
        response.json().get('fact').get('condition'),
        src='en', dest='ru')
    wind_speed = response.json().get('fact').get('wind_speed')
    pressure_mm = response.json().get('fact').get('pressure_mm')
    prec = PREC_TYPE.get(response.json().get('fact').get('prec_type'))
    message = (
        f'Сегодня {translate_date.text}\n'
        f'Температура: {temperature}\n'
        f'Ощущается как {feels_like}\n'
        f'{condition.text.capitalize()}\n'
        f'Скорость ветра: {wind_speed} м/с\n'
        f'Давление: {pressure_mm} мм\n'
        f'{prec}'
    )
    return message


def send_message(message, recipients: list):
    for recipient in recipients:
        params = {
            'chat_id': recipient,
            'text': message
        }
        requests.get(
            url=TG_SEND_MESSAGE,
            params=params
        )


def get_measure_count_argv():
    args = sys.argv
    if len(args) >= 3:
        if args[1] in VALID_ARGS_MEASURE and args[2].isdigit():
            return args[1], int(args[2])
        return None, None
    return None, None


def main(time_measure='h', count=24):
    send_message('Бот запущен!', RECIPIENTS_IDS)
    if time_measure == 'h':
        schedule.every(count).hours.do(
            send_message, get_weather_data(), RECIPIENTS_IDS)
    elif time_measure == 'd':
        schedule.every(count).days.do(
            send_message, get_weather_data(), RECIPIENTS_IDS)
    else:
        schedule.every(count).minutes.do(
            send_message, get_weather_data(), RECIPIENTS_IDS)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    measure, count_measure = get_measure_count_argv()
    first_thread = threading.Thread(target=get_userid_by_updates)
    if measure and count_measure:
        second_thread = threading.Thread(
            target=main, args=[measure, count_measure]
        )
    else:
        second_thread = threading.Thread(target=main)
    first_thread.start()
    second_thread.start()
