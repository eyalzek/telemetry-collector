db-exec:
	docker-compose exec -- db  sh -c 'PGPASSWORD=password psql -U user db'
