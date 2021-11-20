terraform {
  required_version = ">= 1.0.0"
  required_providers {
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.7.0"
    }
    google = {
      source  = "hashicorp/google"
      version = ">= 3.90.0"
    }
  }


  backend "gcs" {
    bucket = "crypto-101-tf-state"
    prefix = "terraform/state"
  }
}