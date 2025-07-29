locals {
  shared_module_version = "bfdcca60d62801acbf61e77f49de25889647b5ef"
}

data "digitalocean_kubernetes_versions" "available_versions" {}

module "main_vpc" {
  source = "git::https://github.com/openedx/openedx-k8s-harmony.git//terraform/modules/digitalocean/vpc?ref=${local.shared_module_version}"

  region       = var.region
  environment  = var.environment

  vpc_ip_range = "10.12.0.0/24"
}

module "kubernetes_cluster" {
  source = "git::https://github.com/openedx/openedx-k8s-harmony.git//terraform/modules/digitalocean/doks?ref=${local.shared_module_version}"

  region      = var.region
  environment = var.environment
  vpc_id      = module.main_vpc.vpc_id

  cluster_name       = var.kubernetes_cluster_name
  kubernetes_version = data.digitalocean_kubernetes_versions.available_versions.latest_version
}

module "kubernetes_cert_manager" {
  depends_on = [module.kubernetes_cluster]

  source                          = "git::https://gitlab.com/opencraft/ops/terraform-modules.git//modules/k8s-cert-manager?ref=v1.0.1"
  namespace                       = "kube-system"
  lets_encrypt_notification_inbox = var.lets_encrypt_notification_inbox
}

module "kubernetes_ingress" {
  depends_on = [module.kubernetes_cluster]

  source            = "git::https://gitlab.com/opencraft/ops/terraform-modules.git//modules/k8s-nginx-ingress?ref=v1.0.1"
  ingress_namespace = "kube-system"
}

module "spaces" {
  source = "git::https://github.com/openedx/openedx-k8s-harmony.git//terraform/modules/digitalocean/spaces?ref=${local.shared_module_version}"

  region      = var.region
  environment = var.environment

  bucket_prefix = "phd-experiment"
}

module "mysql_database" {
  source = "git::https://github.com/openedx/openedx-k8s-harmony.git//terraform/modules/digitalocean/database?ref=${local.shared_module_version}"

  region                  = var.region
  environment             = var.environment
  access_token            = var.do_access_token
  vpc_id                  = module.main_vpc.vpc_id
  kubernetes_cluster_name = var.kubernetes_cluster_name

  database_engine                  = "mysql"
  database_engine_version          = 8
  database_cluster_instances       = 1
  database_cluster_instance_size   = "db-s-1vcpu-1gb"
  database_maintenance_window_day  = "sunday"
  database_maintenance_window_time = "01:00:00"

  # Database cluster firewalls cannot use VPC CIDR, therefore the access is
  # limited to the k8s cluster
  firewall_rules = [
    {
      type  = "k8s"
      value = module.kubernetes_cluster.cluster_id
    },
  ]
}

module "mongodb_database" {
  source = "git::https://github.com/openedx/openedx-k8s-harmony.git//terraform/modules/digitalocean/database?ref=${local.shared_module_version}"

  region                  = var.region
  environment             = var.environment
  access_token            = var.do_access_token
  vpc_id                  = module.main_vpc.vpc_id
  kubernetes_cluster_name = var.kubernetes_cluster_name

  database_engine                  = "mongodb"
  database_engine_version          = 7
  database_cluster_instances       = 3
  database_cluster_instance_size   = "db-s-1vcpu-1gb"
  database_maintenance_window_day  = "sunday"
  database_maintenance_window_time = "1:00"

  # Database cluster firewalls cannot use VPC CIDR, therefore the access is
  # limited to the k8s cluster
  firewall_rules = [
    {
      type  = "k8s"
      value = module.kubernetes_cluster.cluster_id
    },
  ]
}

resource "digitalocean_project" "project" {
  name        = var.kubernetes_cluster_name
  description = "PHD experimentation"
  purpose     = "Web Application"

  resources = [
    module.kubernetes_cluster.cluster_urn,
    module.spaces.bucket_urn,
    module.mysql_database.cluster_urn,
    module.mongodb_database.cluster_urn,
  ]
}

resource "local_sensitive_file" "kubeconfig" {
  filename        = "${path.cwd}/.kubeconfig"
  content         = data.digitalocean_kubernetes_cluster.cluster.kube_config[0].raw_config
  file_permission = "0400"
}
