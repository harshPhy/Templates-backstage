output "topic_arn" {
  description = "ARN of the SNS topic"
  value       = aws_sns_topic.topic.arn
}

output "topic_name" {
  description = "Name of the SNS topic"
  value       = aws_sns_topic.topic.name
}

output "subscription_arns" {
  description = "List of ARNs of the subscriptions"
  value       = aws_sns_topic_subscription.subscriptions[*].arn
}

output "subscription_count" {
  description = "Number of subscriptions to the SNS topic"
  value       = length(var.subscriptions)
} 