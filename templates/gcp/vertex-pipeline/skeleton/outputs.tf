output "pipeline_name" {
  description = "Name of the Vertex AI pipeline"
  value       = var.pipelineName
}

output "pipeline_job_id" {
  description = "ID of the Vertex AI pipeline job"
  value       = google_vertex_ai_pipeline_job.pipeline_job.id
}

output "service_account_email" {
  description = "Email of the service account created for the pipeline"
  value       = google_service_account.vertex_service_account.email
}

output "storage_bucket" {
  description = "Name of the storage bucket for pipeline artifacts"
  value       = google_storage_bucket.pipeline_bucket.name
}

output "pipeline_output_dir" {
  description = "GCS directory for pipeline outputs"
  value       = "gs://${google_storage_bucket.pipeline_bucket.name}/pipeline_output"
}

output "cloud_console_url" {
  description = "URL to view the pipeline in the Google Cloud Console"
  value       = "https://console.cloud.google.com/vertex-ai/pipelines/runs?project=${var.projectId}"
} 