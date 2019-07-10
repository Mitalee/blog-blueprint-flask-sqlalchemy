FROM python:3.6-slim

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev --no-install-recommends

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

LABEL maintainer="Mitalee Mulpuru <raomitalee@gmail.com>"

CMD gunicorn -b 0.0.0.0:8000 --log-level=debug --access-logfile - "blogexample.app:create_app()"