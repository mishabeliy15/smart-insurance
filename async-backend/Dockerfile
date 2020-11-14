FROM python:3.8.5-slim-buster

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get autoclean -yqq \
    && apt-get autoremove -yqq \
    && pip3 install --upgrade pip \
    && mkdir -vp /models


WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/


CMD ["gunicorn", "main:app", "-w", "3", "-k", "uvicorn.workers.UvicornWorker", "-b", ":80"]
