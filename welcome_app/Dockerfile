FROM python:3.8-slim

MAINTAINER Kirill Shmakov 'shmakir@yandex.ru'

ENV FLASK_APP app

WORKDIR /home/welcome_app

COPY app /home/welcome_app/app
COPY requirements.txt /home/welcome_app

RUN pip install -r requirements.txt

CMD ["python3", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5001"]