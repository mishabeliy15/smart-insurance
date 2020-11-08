FROM python:3.8.5-slim-buster

ENV PYTHONUNBUFFERED=1

RUN apt-get update -yqq \
    && apt-get upgrade -yqq \
    && pip3 install --upgrade pip \
    && apt-get install -yqq \
        build-essential \
        python3-dev \
    && apt-get autoclean -yqq \
    && apt-get autoremove -yqq

WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/

# RUN mkdir -vp /usr/src/app/static && ./manage.py collectstatic --noinput << yes

CMD ["uwsgi", "--ini", "uwsgi.ini"]
