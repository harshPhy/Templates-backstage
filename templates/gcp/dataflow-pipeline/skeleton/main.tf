provider "google" {
  project = var.projectId
  region  = var.region
}

# Create a service account for Dataflow
resource "google_service_account" "dataflow_service_account" {
  account_id   = "${var.jobName}-sa"
  display_name = "Service Account for Dataflow job ${var.jobName}"
}

# Grant necessary roles to the service account
resource "google_project_iam_member" "dataflow_worker_role" {
  project = var.projectId
  role    = "roles/dataflow.worker"
  member  = "serviceAccount:${google_service_account.dataflow_service_account.email}"
}

resource "google_project_iam_member" "storage_object_admin" {
  project = var.projectId
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.dataflow_service_account.email}"
}

# Create a Dataflow job from a template
resource "google_dataflow_job" "dataflow_job" {
  name              = var.jobName
  template_gcs_path = var.templatePath
  temp_gcs_location = var.tempLocation
  region            = var.region
  
  parameters = {
    serviceAccount = google_service_account.dataflow_service_account.email
  }
  
  machine_type      = var.machineType
  max_workers       = var.maxWorkers
  network           = var.network
  subnetwork        = var.subnetwork
  service_account_email = google_service_account.dataflow_service_account.email
  
  on_delete = "cancel"
} 