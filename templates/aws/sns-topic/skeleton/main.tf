provider "aws" {
  region = var.region
}

resource "aws_sns_topic" "topic" {
  name         = var.fifoTopic ? "${var.topicName}.fifo" : var.topicName
  display_name = var.displayName
  fifo_topic   = var.fifoTopic

  tags = {
    Name        = var.topicName
    ManagedBy   = "Terraform"
    Source      = "Backstage Template"
  }
}

resource "aws_sns_topic_subscription" "subscriptions" {
  count     = length(var.subscriptions)
  topic_arn = aws_sns_topic.topic.arn
  protocol  = var.subscriptions[count.index].protocol
  endpoint  = var.subscriptions[count.index].endpoint
} 