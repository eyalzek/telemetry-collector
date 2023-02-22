FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN apk add --no-cache build-base libpq-dev &&\
    pip install -r requirements.txt

COPY src/* .

ENTRYPOINT [ 'uvicorn', 'main:app' ]
