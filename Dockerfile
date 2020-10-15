FROM python:3.7.9-slim-buster

RUN mkdir /app
WORKDIR /app

ADD . /app/
ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE 1 \
    PORT=8000
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip3 install pipenv==2020.8.13
RUN pipenv install --dev --system --deploy --skip-lock
RUN python manage.py collectstatic --noinput

CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --log-file -
