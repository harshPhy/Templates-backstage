output "rds_instance_id" {
  description = "The ID of the RDS instance"
  value       = aws_db_instance.postgres_instance.id
}

output "rds_instance_endpoint" {
  description = "The endpoint of the RDS instance"
  value       = aws_db_instance.postgres_instance.endpoint
}

output "rds_instance_port" {
  description = "The port number on which the RDS instance is listening"
  value       = aws_db_instance.postgres_instance.port
}

output "rds_instance_arn" {
  description = "The ARN of the RDS instance"
  value       = aws_db_instance.postgres_instance.arn
}

output "rds_instance_db_name" {
  description = "The name of the initial database created in the RDS instance"
  value       = aws_db_instance.postgres_instance.db_name
}

output "rds_instance_instance_class" {
  description = "The instance class of the RDS instance"
  value       = aws_db_instance.postgres_instance.instance_class
} 