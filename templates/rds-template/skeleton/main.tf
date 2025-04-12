locals {
  # Load and decode the YAML configuration file
  rds_config = yamldecode(file(var.rds_config_file))
}

# Create DB Subnet Group
resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "${local.rds_config["db_subnet_group_name"]}-${var.environment}"
  description = "Subnet group for RDS instance"
  subnet_ids  = var.subnets

  tags = {
    Name = "${var.name}-subnet-group-${var.environment}"
    Environment = var.environment
  }
}

# Create RDS instance
resource "aws_db_instance" "postgres_instance" {
  identifier              = "${var.name}-${var.environment}"
  instance_class          = var.instance_class
  engine                  = "postgres"
  engine_version          = var.engine_version
  allocated_storage       = var.allocated_storage
  storage_type            = var.storage_type
  db_name                 = var.db_name
  username                = var.username
  password                = var.password
  parameter_group_name    = var.parameter_group_name
  backup_retention_period = var.backup_retention_period
  multi_az                = var.multi_az
  publicly_accessible     = var.publicly_accessible
  db_subnet_group_name    = aws_db_subnet_group.db_subnet_group.name
  vpc_security_group_ids  = var.security_groups

  tags = {
    Name        = "${var.name}-${var.environment}"
    Environment = var.environment
    Description = var.description
  }
} 