resource "google_artifact_registry_repository" "telemetry_collector" {
  location      = var.region
  repository_id = "telemetry-collector"
  format        = "DOCKER"
}
