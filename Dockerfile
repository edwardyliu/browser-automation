FROM python:3.6-buster

ENV APP_HOME="/usr/src/app"
RUN apt-get update && apt-get install -y firefox-esr \
 && mkdir -p "${APP_HOME}"

WORKDIR "${APP_HOME}"
COPY . "${APP_HOME}"
RUN pip install -r ./project/server/requirements.txt \
 && python setup.py