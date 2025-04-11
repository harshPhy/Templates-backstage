variable "region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "clusterName" {
  description = "Name of the EMR cluster"
  type        = string
}

variable "description" {
  description = "Description of the EMR cluster"
  type        = string
  default     = ""
}

variable "s3BucketName" {
  description = "Name of the S3 bucket for logs and data"
  type        = string
}

variable "releaseLabel" {
  description = "Amazon EMR release version"
  type        = string
  default     = "emr-6.9.0"
}

variable "applications" {
  description = "List of applications to install on the cluster"
  type        = list(string)
  default     = ["Spark", "Hive", "Livy"]
}

variable "masterInstanceType" {
  description = "Instance type for the master node"
  type        = string
  default     = "m5.xlarge"
}

variable "coreInstanceType" {
  description = "Instance type for core nodes"
  type        = string
  default     = "m5.xlarge"
}

variable "coreInstanceCount" {
  description = "Number of core instances"
  type        = number
  default     = 2
}

variable "sparkJobScript" {
  description = "S3 path to the Spark job script"
  type        = string
  default     = ""
}

variable "keyName" {
  description = "Name of the EC2 key pair to use for SSH access"
  type        = string
  default     = ""
}

variable "subnetId" {
  description = "ID of the subnet to launch the cluster in"
  type        = string
  default     = ""
} 