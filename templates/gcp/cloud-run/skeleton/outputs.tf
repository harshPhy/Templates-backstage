output "service_name" {
  description = "Name of the Cloud Run service"
  value       = google_cloud_run_service.service.name
}

output "service_url" {
  description = "URL of the Cloud Run service"
  value       = google_cloud_run_service.service.status[0].url
}

output "latest_created_revision_name" {
  description = "The latest revision created for this service"
  value       = google_cloud_run_service.service.status[0].latest_created_revision_name
}

output "console_url" {
  description = "URL to view the service in the Google Cloud Console"
  value       = "https://console.cloud.google.com/run/detail/${var.region}/${var.serviceName}/metrics?project=${var.projectId}"
} 