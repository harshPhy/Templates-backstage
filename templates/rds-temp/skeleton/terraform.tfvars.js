// Generated from Backstage template
name                    = "${{ values.name }}"
description             = "${{ values.description }}"
environment             = "${{ values.environment }}"
region                  = "${{ values.region || default('us-east-1') }}"
rds_config_file         = "config/rds-config.yaml"

// Database configuration
instance_class          = "${{ values.instance_class }}"
engine_version          = "${{ values.engine_version }}"
allocated_storage       = "${{ values.allocated_storage || dump }}"
storage_type            = "${{ values.storage_type }}"
db_name                 = "${{ values.db_name }}"
username                = "${{ values.username }}"
parameter_group_name    = "${{ values.parameter_group_name }}"

// Availability & backup
multi_az                = "${{ values.multi_az || dump }}"
publicly_accessible     = "${{ values.publicly_accessible || dump }}"
backup_retention_period = "${{ values.backup_retention_period || dump }}"

// Network configuration
vpc_id                  = "${{ values.vpc_id }}"
subnets                 = "${{ values.subnets || dump }}"
security_groups         = "${{ values.security_groups || dump }}"

// Password - Use environment variable or secrets manager in production
password                = "${{ secrets.DB_PASSWORD || default('${env.DB_PASSWORD}') }}"
