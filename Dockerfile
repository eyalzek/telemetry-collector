FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt .

# RUN apk add --no-cache build-base libpq-dev &&\
RUN pip install -r requirements.txt

COPY bin/docker-entrypoint.sh /usr/bin/
COPY src/* /usr/src/app/

ENTRYPOINT [ "docker-entrypoint.sh", "uvicorn", "--port=8080", "main:app" ]
