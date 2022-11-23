import os
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

TG_SEND_MESSAGE = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage'
YANDEX_WEATHER_API = 'https://api.weather.yandex.ru/v2/forecast?'

ICON_TEMPLATE = 'https://yastatic.net/weather/i/icons/funky/dark/{}.svg'

PREC_TYPE = {
    0: 'Без осадков',
    1: 'Дождь',
    2: 'Дождь со снегом',
    3: 'Снег',
    4: 'Град'
}

translator = Translator()


def get_weather_data():
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


def main():
    schedule.every().day.at('11:00').do(
        send_message, get_weather_data(), RECIPIENTS_IDS)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
