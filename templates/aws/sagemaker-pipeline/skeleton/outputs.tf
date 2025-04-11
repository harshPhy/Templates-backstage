output "pipeline_arn" {
  description = "ARN of the SageMaker pipeline"
  value       = aws_sagemaker_pipeline.pipeline.arn
}

output "pipeline_name" {
  description = "Name of the SageMaker pipeline"
  value       = aws_sagemaker_pipeline.pipeline.pipeline_name
}

output "creation_time" {
  description = "Creation time of the SageMaker pipeline"
  value       = aws_sagemaker_pipeline.pipeline.creation_time
}

output "console_url" {
  description = "URL to view the pipeline in the AWS Console"
  value       = "https://console.aws.amazon.com/sagemaker/home?region=${var.region}#/pipelines/details/${aws_sagemaker_pipeline.pipeline.pipeline_name}"
} 