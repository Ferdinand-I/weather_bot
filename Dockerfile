FROM python:3.7-slim

ENV TZ=Europe/Moscow

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "weather_sender.py"]