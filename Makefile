DC = docker-compose

build:
	$(DC) build

up:
	$(DC) up

clean:
	$(DC) down -v

db-query:
	$(DC) exec -- db  sh -c 'PGPASSWORD=password psql -U user requests'

terraform-state-bucket:
	gsutil ls -b gs://$$(gcloud config get core/project)-terraform-state-store || gsutil mb -l europe-west1 gs://$$(gcloud config get core/project)-terraform-state-store
