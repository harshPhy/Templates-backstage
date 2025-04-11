variable "region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "topicName" {
  description = "Name of the SNS topic"
  type        = string
}

variable "displayName" {
  description = "Display name of the SNS topic"
  type        = string
  default     = ""
}

variable "subscriptions" {
  description = "List of subscriptions to the SNS topic"
  type = list(object({
    protocol = string
    endpoint = string
  }))
  default = []
}

variable "fifoTopic" {
  description = "Whether the topic is a FIFO (First-In-First-Out) topic"
  type        = bool
  default     = false
} 