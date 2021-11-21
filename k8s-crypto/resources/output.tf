output "cluster-name" {
  value     = module.gke
  sensitive = true
}

output "namespace" {
  value     = kubectl_manifest.namespace
  sensitive = true
}

output "argocd" {
  value     = kubectl_manifest.argocd
  sensitive = true
}

output "mongodb" {
  value     = kubectl_manifest.mongodb
  sensitive = true
}

output "airflow" {
  value     = kubectl_manifest.airflow
  sensitive = true
}