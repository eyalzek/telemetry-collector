#!/bin/sh

while ! nc -z ${DATABASE_HOST} 5432; do echo "Waiting for DB host: ${DATABASE_HOST}..." && sleep 3; done

exec "$@"
