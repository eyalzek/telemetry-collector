provider "google" {
  project = var.project_id
}

data "google_project" "project" {
}

# Bucket name is unfortunately hard-coded
terraform {
  required_version = ">=1.3"

  required_providers {
    google = {
      version = ">= 4.0"
      source = "hashicorp/google"
    }
  }

  backend "gcs" {
    bucket  = "test-eyal-terraform-state-store"
    prefix  = "telemetry-collector"
  }
}
