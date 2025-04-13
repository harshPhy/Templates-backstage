variable "rds_config_file" {
  description = "Path to the YAML file containing the RDS configuration"
  type        = string
  default     = "config/rds-config.yaml"
}

variable "name" {
  description = "Name for the RDS instance (will be suffixed with environment)"
  type        = string
}

variable "description" {
  description = "Description for this RDS deployment"
  type        = string
  default     = "PostgreSQL RDS instance deployed via Backstage"
}

variable "environment" {
  description = "Deployment Environment"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "username" {
  description = "Database master username"
  type        = string
}

variable "password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}

variable "vpc_id" {
  description = "VPC ID for RDS instance"
  type        = string
}

variable "subnets" {
  description = "Subnet IDs for RDS instance"
  type        = list(string)
}

variable "security_groups" {
  description = "Security group IDs for RDS instance"
  type        = list(string)
}

variable "instance_class" {
  description = "RDS instance class"
  type        = string
}

variable "engine_version" {
  description = "Version of PostgreSQL to deploy"
  type        = string
}

variable "allocated_storage" {
  description = "Allocated storage in GB"
  type        = number
}

variable "storage_type" {
  description = "Type of storage for the RDS instance"
  type        = string
  default     = "gp2"
}

variable "db_name" {
  description = "Name of the initial database to create"
  type        = string
}

variable "parameter_group_name" {
  description = "Parameter group name"
  type        = string
  default     = "default.postgres15"
}

variable "multi_az" {
  description = "Whether to enable Multi-AZ deployment"
  type        = boolean
  default     = false
}

variable "publicly_accessible" {
  description = "Whether the database should be publicly accessible"
  type        = boolean
  default     = false
}

variable "backup_retention_period" {
  description = "Number of days to retain backups"
  type        = number
  default     = 7
} 