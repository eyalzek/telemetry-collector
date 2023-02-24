locals {
  service_name = "telemetry-collector"
  docker_image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.telemetry_collector.name}/collector:$COMMIT_SHA"
}

resource "google_project_iam_member" "cloubuild_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
}

resource "google_project_iam_member" "cloubuild_sa_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
}

resource "google_cloudbuild_trigger" "telemetry_pipeline" {
  location = var.region
  name     = "telemetry-pipeline"

  github {
    owner = "eyalzek"
    name  = "telemetry-collector"
    push {
      branch = "^feature/async-try1$"
    }
  }

  build {
    step {
      name = "gcr.io/cloud-builders/docker"
      args = ["build", "-t", local.docker_image, "."]
    }

    step {
      name = "gcr.io/cloud-builders/docker"
      args = ["push", local.docker_image]
    }

    step {
      name       = "gcr.io/google.com/cloudsdktool/cloud-sdk"
      entrypoint = "gcloud"
      args = ["run", "deploy", local.service_name, "--image", local.docker_image,
        "--region", var.region, "--vpc-connector", google_vpc_access_connector.connector.name,
        "--set-env-vars=DATABASE_HOST=${google_sql_database_instance.telemetry.private_ip_address},DATABASE_USER=${google_sql_user.telemetry_user.name}",
        "--set-secrets=DATABASE_PASSWORD=${google_secret_manager_secret.telemetry.secret_id}:${google_secret_manager_secret_version.telemetry_db.version}"
      ]
    }
  }
}
