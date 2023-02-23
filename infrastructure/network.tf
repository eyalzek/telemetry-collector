resource "google_compute_network" "telemetry_network" {
  name = "telemetry-network"
}

resource "google_vpc_access_connector" "connector" {
  name          = "vpc-connector"
  region        = var.region
  ip_cidr_range = "10.8.0.0/28"
  network       = google_compute_network.telemetry_network.id
}

resource "google_compute_global_address" "private_ip_address" {
  name          = "telemetry-private-ip-address"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.telemetry_network.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.telemetry_network.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}
