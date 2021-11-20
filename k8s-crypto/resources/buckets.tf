resource "google_storage_bucket" "bucket" {
  for_each = toset(var.buckets)
  name     = "${each.key}-${var.project_id}"
  location = var.region
  project  = var.project_id

}

resource "google_storage_bucket_object" "objects" {
  for_each = fileset("../objects/", "*")

  bucket = "landing-${var.project_id}"
  name   = "vini_folder/${each.key}"
  source = "../objects/${each.key}"

  depends_on = [
    google_storage_bucket.bucket,
    google_project_service.project
  ]
}
