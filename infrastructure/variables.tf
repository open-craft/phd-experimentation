variable "do_access_token" {
  type        = string
  description = "DitialOcean access token."
  sensitive   = true
}

variable "do_spaces_access_id" {
  type        = string
  description = "DigitalOcean Spaces access key ID."
  sensitive   = true
}

variable "do_spaces_secret_key" {
  type        = string
  description = "DigitalOcean Spaces secret access key."
  sensitive   = true
}

variable "kubernetes_cluster_name" {
  type        = string
  description = "Name of the DigitalOcean Kubernetes cluster to create."
}

variable "region" {
  type        = string
  description = "DigitalOcean region to create the resources in."
  validation {
    condition = contains([
      "ams3",
      "blr1",
      "fra1",
      "lon1",
      "nyc3",
      "sfo2",
      "sfo3",
      "sgp1",
      "syd1",
      "tor1",
    ], var.region)
    error_message = "The DigitalOcean region must be in the acceptable region list."
  }
}

variable "environment" {
  type        = string
  description = "The DigitalOcean project environment. (for example: production, staging, development, etc.)"
}

variable "lets_encrypt_notification_inbox" {
  type        = string
  description = "The email address to receive notifications from Let's Encrypt."
}
