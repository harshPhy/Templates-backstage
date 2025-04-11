provider "google" {
  project = var.projectId
  region  = var.region
}

resource "google_project_service" "run_api" {
  service = "run.googleapis.com"

  disable_on_destroy = false
}

resource "google_project_service" "iam_api" {
  service = "iam.googleapis.com"

  disable_on_destroy = false
}

resource "google_cloud_run_service" "service" {
  name     = var.serviceName
  location = var.region

  metadata {
    annotations = {
      "run.googleapis.com/launch-stage" = "BETA"
      "run.googleapis.com/description"  = var.description
    }
  }

  template {
    spec {
      containers {
        image = var.image
        
        resources {
          limits = {
            cpu    = var.cpu
            memory = var.memory
          }
        }
      }
    }
    
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = var.maxInstances
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [google_project_service.run_api]
}

# Make the service publicly accessible
resource "google_cloud_run_service_iam_member" "public_access" {
  service  = google_cloud_run_service.service.name
  location = google_cloud_run_service.service.location
  role     = "roles/run.invoker"
  member   = "allUsers"
} 