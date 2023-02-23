resource "google_sql_database_instance" "telemetry" {
  name             = "telemetry-instance"
  region           = var.region
  database_version = "POSTGRES_14"

  depends_on = [google_service_networking_connection.private_vpc_connection]

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled                                  = false
      private_network                               = google_compute_network.telemetry_network.id
      enable_private_path_for_google_cloud_services = true
    }
  }
}

resource "google_sql_database" "requests" {
  name     = "requests"
  instance = google_sql_database_instance.telemetry.name
}

resource "random_password" "password" {
  length  = 24
  special = true
}

resource "google_sql_user" "telemetry_user" {
  name     = "telemetry"
  instance = google_sql_database_instance.telemetry.name
  password = random_password.password.result
}
