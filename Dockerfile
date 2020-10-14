FROM python:3.7.9

RUN mkdir /app
WORKDIR /app

ADD . /app/
ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE 1 \
    LANG C.UTF-8 \
    PORT=8000
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        libpq-dev \
        && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip3 install pipenv==2020.8.13
RUN pipenv install --dev --system --deploy --skip-lock
RUN python manage.py collectstatic --noinput

#EXPOSE 8000
CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --log-file -
