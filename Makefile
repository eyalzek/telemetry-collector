DC = docker-compose

build:
	$(DC) build

up:
	$(DC) up

clean:
	$(DC) down -v

db-query:
	$(DC) exec -- db  sh -c 'PGPASSWORD=password psql -U user requests'
