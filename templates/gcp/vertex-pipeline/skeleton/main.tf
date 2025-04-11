provider "google" {
  project = var.projectId
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "aiplatform_api" {
  service = "aiplatform.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "iam_api" {
  service = "iam.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "compute_api" {
  service = "compute.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "container_api" {
  service = "container.googleapis.com"
  disable_on_destroy = false
}

# IAM Service Account for Vertex AI
resource "google_service_account" "vertex_service_account" {
  account_id   = "${var.pipelineName}-sa"
  display_name = "Service Account for Vertex AI Pipeline ${var.pipelineName}"
  
  depends_on = [google_project_service.iam_api]
}

# Grant necessary roles to the service account
resource "google_project_iam_member" "vertex_service_account_roles" {
  for_each = toset([
    "roles/aiplatform.user",
    "roles/storage.objectAdmin",
    "roles/logging.logWriter",
    "roles/artifactregistry.reader"
  ])
  
  project = var.projectId
  role    = each.key
  member  = "serviceAccount:${google_service_account.vertex_service_account.email}"
  
  depends_on = [google_service_account.vertex_service_account]
}

# Create a GCS bucket for pipeline artifacts
resource "google_storage_bucket" "pipeline_bucket" {
  name          = "${var.projectId}-${var.pipelineName}-bucket"
  location      = var.region
  force_destroy = true
  
  uniform_bucket_level_access = true
  
  depends_on = [google_project_service.aiplatform_api]
}

# Create a Vertex AI Pipeline job
resource "google_vertex_ai_pipeline_job" "pipeline_job" {
  display_name = var.pipelineName
  location     = var.region
  
  pipeline_spec {
    pipeline_manifest = file(var.pipelineSpecPath)
  }
  
  runtime_config {
    gcs_output_directory = "gs://${google_storage_bucket.pipeline_bucket.name}/pipeline_output"
    
    parameter_values = {
      project_id    = var.projectId
      location      = var.region
      machine_type  = var.machineType
      service_account = google_service_account.vertex_service_account.email
    }
  }
  
  service_account = google_service_account.vertex_service_account.email
  
  network = var.network
  
  depends_on = [
    google_project_service.aiplatform_api,
    google_storage_bucket.pipeline_bucket,
    google_project_iam_member.vertex_service_account_roles
  ]
} 