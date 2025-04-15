${{ values.name }} - AWS RDS PostgreSQL Module

${{ values.description }}

This Terraform module creates an AWS RDS PostgreSQL instance based on the configuration provided.

## Configuration

The RDS instance is configured as follows:

- **Name**: ${{ values.name }}
- **Environment**: ${{ values.environment }}
- **Database Engine**: PostgreSQL ${{ values.engine_version }}
- **Instance Class**: ${{ values.instance_class }}
- **Storage**: ${{ values.allocated_storage }}GB (${{ values.storage_type }})
- **Database Name**: ${{ values.db_name }}
- **Multi-AZ**: ${{ values.multi_az }}
- **Publicly Accessible**: ${{ values.publicly_accessible }}
- **Backup Retention Period**: ${{ values.backup_retention_period }} days

## Prerequisites

Before you can apply this Terraform configuration, you'll need:

1. AWS credentials configured with appropriate permissions
2. A VPC with at least 2 subnets (for Multi-AZ deployment)
3. Security groups that allow access to PostgreSQL (port 5432)

## Getting Started

1. Review and update the `terraform.tfvars` file with your specific configuration:

   - Update VPC, subnet, and security group IDs
   - Set a secure password for the database

2. Initialize Terraform:

   ```
   terraform init
   ```

3. Plan the deployment:

   ```
   terraform plan
   ```

4. Apply the changes:
   ```
   terraform apply
   ```

## Security Considerations

- The password is stored in plain text in the `terraform.tfvars` file. For production environments, consider using AWS Secrets Manager or another secure method.
- By default, the RDS instance is not publicly accessible unless you've changed the configuration.
- Make sure your security groups only allow access from trusted sources.

## Outputs

After applying this Terraform configuration, you'll receive the following outputs:

- RDS instance ID
- RDS endpoint and port
- RDS ARN
- Database name
- Instance class
