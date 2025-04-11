provider "google" {
  project = var.projectId
  region  = var.region
  zone    = var.zone
}

# Enable required APIs
resource "google_project_service" "container_api" {
  service = "container.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "compute_api" {
  service = "compute.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "iam_api" {
  service = "iam.googleapis.com"
  disable_on_destroy = false
}

# Create a GKE cluster
resource "google_container_cluster" "gke_cluster" {
  name     = var.clusterName
  location = var.zone
  
  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1
  
  # Specify the Kubernetes version
  min_master_version = var.kubernetesVersion
  
  # Enable workload identity for better security
  workload_identity_config {
    workload_pool = "${var.projectId}.svc.id.goog"
  }
  
  depends_on = [
    google_project_service.container_api,
    google_project_service.compute_api
  ]
}

# Create a node pool for the GKE cluster
resource "google_container_node_pool" "primary_nodes" {
  name       = "${var.clusterName}-node-pool"
  location   = var.zone
  cluster    = google_container_cluster.gke_cluster.name
  node_count = var.nodeCount
  
  node_config {
    machine_type = var.machineType
    
    # Google recommended metadata
    metadata = {
      disable-legacy-endpoints = "true"
    }
    
    # Needed for using workload identity
    workload_metadata_config {
      mode = "GKE_METADATA"
    }
    
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

# Kubeflow installation will be done via Helm after the cluster is created
# This is a local-exec provisioner that will:
# 1. Get credentials for the GKE cluster
# 2. Install Kubeflow using kustomize
resource "null_resource" "install_kubeflow" {
  provisioner "local-exec" {
    command = <<-EOT
      gcloud container clusters get-credentials ${google_container_cluster.gke_cluster.name} --zone ${var.zone} --project ${var.projectId}
      
      # Install Kubeflow Pipelines using Kustomize
      curl -s "https://raw.githubusercontent.com/kubeflow/pipelines/v${var.kubeflowVersion}/manifests/kustomize/cluster-scoped-resources/kustomization.yaml" | sed "s/namespace: kubeflow/namespace: kubeflow/g" > kustomization.yaml
      kubectl apply -k .
      
      # Install the Kubeflow Pipelines
      curl -s "https://raw.githubusercontent.com/kubeflow/pipelines/v${var.kubeflowVersion}/manifests/kustomize/env/platform-agnostic/kustomization.yaml" > kustomization.yaml
      kubectl apply -k .
    EOT
  }
  
  depends_on = [google_container_node_pool.primary_nodes]
} 