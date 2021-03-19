FROM python:3.8-slim

MAINTAINER Kirill Shmakov 'shmakir@yandex.ru'

ENV FLASK_APP app

WORKDIR /home/notes_app

COPY app /home/notes_app/app
COPY requirements.txt /home/notes_app

COPY notes /home/notes_app/notes
COPY convert_mds.py /home/notes_app

ENV PYTHONPATH "${PYTHONPATH}:/home/notes_app/app"

RUN pip install -r requirements.txt
RUN ./convert_mds.py

CMD ["python3", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5003"]