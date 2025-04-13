variable "name" {
  description = "Name for the RDS resources"
  type        = string
}

variable "description" {
  description = "Description of the RDS resources"
  type        = string
}

variable "environment" {
  description = "Deployment Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "rds_config_file" {
  description = "Path to the YAML file containing the RDS configuration"
  type        = string
  default     = "config/rds-config.yaml"
}

# Database Configuration
variable "instance_class" {
  description = "RDS instance class"
  type        = string
}

variable "engine_version" {
  description = "PostgreSQL engine version"
  type        = string
}

variable "allocated_storage" {
  description = "Allocated storage size in GB"
  type        = number
}

variable "storage_type" {
  description = "Type of storage (gp2, gp3, io1)"
  type        = string
  default     = "gp2"
}

variable "db_name" {
  description = "Name of the database"
  type        = string
}

variable "username" {
  description = "Master username for the RDS instance"
  type        = string
}

variable "password" {
  description = "Master password for the RDS instance"
  type        = string
  sensitive   = true
}

variable "parameter_group_name" {
  description = "Parameter group name"
  type        = string
}

# Availability and Backup
variable "multi_az" {
  description = "Whether to enable Multi-AZ deployment"
  type        = bool
  default     = false
}

variable "publicly_accessible" {
  description = "Whether the database should be publicly accessible"
  type        = bool
  default     = false
}

variable "backup_retention_period" {
  description = "Number of days to retain backups"
  type        = number
  default     = 7
}

# Network Configuration
variable "vpc_id" {
  description = "VPC ID where the RDS instance will be deployed"
  type        = string
}

variable "subnets" {
  description = "List of subnet IDs where the RDS instance will be deployed"
  type        = list(string)
}

variable "security_groups" {
  description = "List of security group IDs for the RDS instance"
  type        = list(string)
} 