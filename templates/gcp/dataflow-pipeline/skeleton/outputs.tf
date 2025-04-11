output "job_name" {
  description = "Name of the Dataflow job"
  value       = google_dataflow_job.dataflow_job.name
}

output "job_id" {
  description = "ID of the Dataflow job"
  value       = google_dataflow_job.dataflow_job.id
}

output "job_state" {
  description = "State of the Dataflow job"
  value       = google_dataflow_job.dataflow_job.state
}

output "service_account_email" {
  description = "Email of the service account running the Dataflow job"
  value       = google_service_account.dataflow_service_account.email
}

output "dataflow_console_url" {
  description = "URL to view the Dataflow job in the Google Cloud Console"
  value       = "https://console.cloud.google.com/dataflow/jobs/${var.region}/${google_dataflow_job.dataflow_job.id}?project=${var.projectId}"
} 