resource "google_secret_manager_secret" "telemetry" {
  secret_id = "telemetry"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "telemetry_db" {
  secret = google_secret_manager_secret.telemetry.id

  secret_data = random_password.password.result
}
