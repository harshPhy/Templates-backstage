output "cluster_id" {
  description = "ID of the EMR cluster"
  value       = aws_emr_cluster.spark_cluster.id
}

output "cluster_name" {
  description = "Name of the EMR cluster"
  value       = aws_emr_cluster.spark_cluster.name
}

output "master_public_dns" {
  description = "Public DNS of the master node"
  value       = aws_emr_cluster.spark_cluster.master_public_dns
}

output "log_uri" {
  description = "URI for EMR cluster logs in S3"
  value       = aws_emr_cluster.spark_cluster.log_uri
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket for logs and data"
  value       = aws_s3_bucket.emr_bucket.bucket
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.emr_bucket.arn
}

output "emr_console_url" {
  description = "URL to view the cluster in the AWS Console"
  value       = "https://console.aws.amazon.com/elasticmapreduce/home?region=${var.region}#cluster-details:${aws_emr_cluster.spark_cluster.id}"
} 