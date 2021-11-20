variable "region" {
  default = "us-east1"
}

variable "project_id" {
  default = "crypto-101-332715"
}

variable "buckets" {
  type    = list(string)
  default = ["landing", "processing", "curated", "codes"]

}

variable "cluster_name" {
  default = "cluster-gke-crypto"
}

variable "env_name" {
  default = "uat"
}

variable "network" {
  default = "gke-crypto-network"
}

variable "subnetwork" {
  default = "gke-crypto-subnet"
}

variable "ip_pods_name" {
  default = "range-ip-pods"
}

variable "ip_service_name" {
  default = "range-ip-service"
}


variable "services" {
  type = list(string)
  default = [
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "networkservices.googleapis.com",
    "cloudbuild.googleapis.com",
    "cloudbilling.googleapis.com",
    "compute.googleapis.com",
    "container.googleapis.com"
  ]
}