module "gcp-network" {
  source       = "terraform-google-modules/network/google"
  version      = "~> 2.5"
  depends_on   = [google_project_service.project]
  project_id   = var.project_id
  network_name = "${var.network}-${var.env_name}"
  subnets = [
    {
      subnet_name   = "${var.subnetwork}-${var.env_name}"
      subnet_ip     = "10.10.0.0/16"
      subnet_region = var.region
    },
  ]
  secondary_ranges = {
    "${var.subnetwork}-${var.env_name}" = [
      {
        range_name    = var.ip_pods_name
        ip_cidr_range = "10.20.0.0/16"
      },
      {
        range_name    = var.ip_service_name
        ip_cidr_range = "10.30.0.0/16"
      },
    ]
  }
}

module "gke" {
  source                     = "terraform-google-modules/kubernetes-engine/google//modules/private-cluster"
  depends_on                 = [google_project_service.project]
  project_id                 = var.project_id
  name                       = "${var.cluster_name}-${var.env_name}"
  regional                   = true
  region                     = var.region
  network                    = module.gcp-network.network_name
  subnetwork                 = module.gcp-network.subnets_names[0]
  ip_range_pods              = var.ip_pods_name
  ip_range_services          = var.ip_service_name
  horizontal_pod_autoscaling = true
  node_pools = [
    {
      name           = "node-pool"
      machine_type   = "e2-medium"
      node_locations = "us-east1-b"
      min_count      = 3
      max_count      = 12
      disk_size_gb   = 30,
      autoscaling    = true,
      auto_repair    = true
      auto_upgrade   = true
    },
  ]
}

module "gke_auth" {
  source       = "terraform-google-modules/kubernetes-engine/google//modules/auth"
  depends_on   = [module.gke]
  project_id   = var.project_id
  location     = module.gke.location
  cluster_name = module.gke.name
}

resource "local_file" "kubeconfig" {
  content    = module.gke_auth.kubeconfig_raw
  filename   = "kubeconfig-${var.env_name}"
  depends_on = [google_project_service.project]
}


