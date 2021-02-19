#!/usr/bin/env docker-builder
# IMAGE: docker.io/own3dh2so4/xiaomi-mi-temperature:0.0.2

FROM python:3.9.1-alpine3.12

RUN apk add build-base bluez glib-dev && \
    mkdir -p /var/log/cron && \
    touch /var/log/cron/cron.log

RUN pip3 install pipenv==2020.8.13

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN set -ex && pipenv install --deploy --system

COPY ./app /app/app

COPY crontab/crontab /crontab
COPY crontab/start.sh /start.sh

CMD ["./start.sh"]
