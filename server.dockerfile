FROM python:slim-buster

WORKDIR /var/www/application

RUN apt update && apt install -y gcc

#RUN curl -sL -o /tmp/wsgi.tar.gz https://projects.unbit.it/downloads/uwsgi-2.0.tar.gz
#RUN tar zxvf /tmp/wsgi.tar.gz -C /tmp/
#RUN make -C /tmp/uwsgi-2.0

RUN pip install --upgrade uwsgi gunicorn requests bs4 flask lxml

COPY ./server.py ./server.py
COPY ./wsgi.py ./wsgi.py
COPY ./models/logger.py ./models/logger.py
COPY ./models/notifications/ ./models/notifications/
COPY ./models/config.py ./models/config.py
COPY ./models/webhook_message.py ./models/webhook_message.py
COPY ./templates/ ./templates/
COPY ./res/roles.json ./res/roles.json
COPY ./res/twitch_config.json ./res/twitch_config.json
COPY ./res/notifications_config.json ./res/notifications_config.json
CMD ["gunicorn","--bind", "0.0.0.0:5000", "--workers", "1", "wsgi:app"]



