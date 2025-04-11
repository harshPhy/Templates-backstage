output "endpoint_name" {
  description = "Name of the SageMaker endpoint"
  value       = aws_sagemaker_endpoint.endpoint.name
}

output "endpoint_arn" {
  description = "ARN of the SageMaker endpoint"
  value       = aws_sagemaker_endpoint.endpoint.arn
}

output "endpoint_status" {
  description = "Status of the SageMaker endpoint"
  value       = aws_sagemaker_endpoint.endpoint.status
}

output "model_name" {
  description = "Name of the SageMaker model"
  value       = aws_sagemaker_model.model.name
}

output "model_arn" {
  description = "ARN of the SageMaker model"
  value       = aws_sagemaker_model.model.arn
}

output "endpoint_config_name" {
  description = "Name of the SageMaker endpoint configuration"
  value       = aws_sagemaker_endpoint_configuration.endpoint_config.name
}

output "endpoint_url" {
  description = "URL for making requests to the SageMaker endpoint"
  value       = "https://runtime.sagemaker.${var.region}.amazonaws.com/endpoints/${aws_sagemaker_endpoint.endpoint.name}/invocations"
} 