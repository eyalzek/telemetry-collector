FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN apk add --no-cache build-base libpq-dev &&\
    pip install -r requirements.txt

COPY bin/docker-entrypoint.sh /usr/bin/
COPY src/* .

ENTRYPOINT [ 'docker-entrypoint.sh', 'uvicorn', 'main:app' ]
