provider "kubectl" {
  host                   = module.gke_auth.host
  cluster_ca_certificate = module.gke_auth.cluster_ca_certificate
  token                  = module.gke_auth.token
  load_config_file       = false
}

data "kubectl_file_documents" "namespace" {
  content = file("../charts/argocd/namespace.yaml")
}
resource "kubectl_manifest" "namespace" {
  count              = length(data.kubectl_file_documents.namespace.documents)
  yaml_body          = element(data.kubectl_file_documents.namespace.documents, count.index)
  override_namespace = "argocd"
  depends_on = [
    data.kubectl_file_documents.namespace
  ]
}

data "kubectl_file_documents" "argocd" {
  content = file("../charts/argocd/install.yaml")
}


resource "kubectl_manifest" "argocd" {
  depends_on         = [kubectl_manifest.namespace, data.kubectl_file_documents.argocd]
  count              = length(data.kubectl_file_documents.argocd.documents)
  yaml_body          = element(data.kubectl_file_documents.argocd.documents, count.index)
  override_namespace = "argocd"
}

data "kubectl_file_documents" "airflow" {
  content = file("../apps/airflow-app.yaml")
}

resource "kubectl_manifest" "airflow" {
  depends_on = [
    kubectl_manifest.argocd,
  ]
  count              = length(data.kubectl_file_documents.airflow.documents)
  yaml_body          = element(data.kubectl_file_documents.airflow.documents, count.index)
  override_namespace = "argocd"
}

data "kubectl_file_documents" "mongodb" {
  content = file("../apps/mongodb-app.yaml")
}

resource "kubectl_manifest" "mongodb" {
  depends_on = [
    kubectl_manifest.argocd,
  ]
  count              = length(data.kubectl_file_documents.mongodb.documents)
  yaml_body          = element(data.kubectl_file_documents.mongodb.documents, count.index)
  override_namespace = "argocd"
}

data "kubectl_file_documents" "binancelistener" {
  content = file("../apps/binance-listener-app.yaml")
}

resource "kubectl_manifest" "binancelistener" {
  depends_on = [
    kubectl_manifest.argocd,
  ]
  count              = length(data.kubectl_file_documents.binancelistener.documents)
  yaml_body          = element(data.kubectl_file_documents.binancelistener.documents, count.index)
  override_namespace = "argocd"
}