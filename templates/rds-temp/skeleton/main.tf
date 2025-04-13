provider "aws" {
  region = var.region
}

locals {
  # Load and decode the YAML configuration file
  rds_config = yamldecode(file(var.rds_config_file))
}

# Create DB Subnet Group
resource "aws_db_subnet_group" "db_subnet_group" {
  name        = "${local.rds_config.db_subnet_group_name}-${var.environment}"
  description = "Subnet group for RDS instance - ${var.description}"
  subnet_ids  = var.subnets

  tags = local.rds_config.tags
}

# Create RDS instance
resource "aws_db_instance" "rds_instance" {
  identifier              = "${local.rds_config.identifier}-${var.environment}"
  instance_class          = local.rds_config.instance_class
  engine                  = local.rds_config.engine
  engine_version          = local.rds_config.engine_version
  allocated_storage       = local.rds_config.allocated_storage
  storage_type            = local.rds_config.storage_type
  db_name                 = local.rds_config.db_name
  username                = var.username
  password                = var.password
  parameter_group_name    = var.parameter_group_name
  backup_retention_period = var.backup_retention_period
  multi_az                = var.multi_az
  publicly_accessible     = var.publicly_accessible
  db_subnet_group_name    = aws_db_subnet_group.db_subnet_group.name
  vpc_security_group_ids  = var.security_groups

  tags = merge(
    local.rds_config.tags,
    {
      Name = "${local.rds_config.identifier}-${var.environment}"
    }
  )
}

# Outputs
output "rds_endpoint" {
  description = "The connection endpoint for the RDS instance"
  value       = aws_db_instance.rds_instance.endpoint
}

output "db_name" {
  description = "The database name"
  value       = aws_db_instance.rds_instance.db_name
}

output "db_port" {
  description = "The database port"
  value       = aws_db_instance.rds_instance.port
}

output "resource_id" {
  description = "The RDS Resource ID"
  value       = aws_db_instance.rds_instance.resource_id
} 