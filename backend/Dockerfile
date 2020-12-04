FROM python:3.8.5-slim-buster

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update -yqq \
    && apt-get upgrade -yqq \
    && pip3 install --upgrade pip \
    && apt-get install -yqq \
        build-essential \
        python3-dev \
        apt-utils \
        binutils \
        libproj-dev \
        gdal-bin \
        git \
    && apt-get autoclean -yqq \
    && apt-get autoremove -yqq

RUN apt-get update && apt-get install -yqq wget lsb-release
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update && apt-get install -yqq postgresql-client-13

WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
#RUN pip install git+https://github.com/mjs7231/django-dbbackup.git#egg=django-dbbackup

COPY . /usr/src/app/

# RUN mkdir -vp /usr/src/app/static && ./manage.py collectstatic --noinput << yes

CMD ["uwsgi", "--ini", "uwsgi.ini"]
