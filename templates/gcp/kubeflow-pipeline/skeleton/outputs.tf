output "cluster_name" {
  description = "Name of the GKE cluster"
  value       = google_container_cluster.gke_cluster.name
}

output "cluster_endpoint" {
  description = "Endpoint for GKE control plane"
  value       = google_container_cluster.gke_cluster.endpoint
  sensitive   = true
}

output "cluster_ca_certificate" {
  description = "Public certificate of the cluster's certificate authority"
  value       = base64decode(google_container_cluster.gke_cluster.master_auth[0].cluster_ca_certificate)
  sensitive   = true
}

output "kubeflow_instructions" {
  description = "Instructions for accessing Kubeflow"
  value       = "To access Kubeflow UI, run: kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80 and open http://localhost:8080 in your browser"
}

output "get_credentials_command" {
  description = "Command to get credentials for the GKE cluster"
  value       = "gcloud container clusters get-credentials ${google_container_cluster.gke_cluster.name} --zone ${var.zone} --project ${var.projectId}"
}

output "cloud_console_url" {
  description = "URL to view the GKE cluster in the Google Cloud Console"
  value       = "https://console.cloud.google.com/kubernetes/clusters/details/${var.zone}/${google_container_cluster.gke_cluster.name}?project=${var.projectId}"
}

output "node_pool_name" {
  description = "Name of the GKE node pool"
  value       = google_container_node_pool.primary_nodes.name
}

output "kubeflow_version" {
  description = "Installed version of Kubeflow"
  value       = var.kubeflowVersion
}

output "kubernetes_version" {
  description = "Kubernetes version running on the cluster"
  value       = var.kubernetesVersion
}

output "node_machine_type" {
  description = "Machine type used for the cluster nodes"
  value       = var.machineType
}

output "workload_identity_enabled" {
  description = "Indicates that workload identity is enabled on this cluster"
  value       = "true"
} 