provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "emr_bucket" {
  bucket = var.s3BucketName
  force_destroy = true

  tags = {
    Name        = var.s3BucketName
    Description = var.description
    ManagedBy   = "Terraform"
    Source      = "Backstage Template"
  }
}

resource "aws_s3_bucket_ownership_controls" "emr_bucket_ownership" {
  bucket = aws_s3_bucket.emr_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "emr_bucket_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.emr_bucket_ownership]
  bucket = aws_s3_bucket.emr_bucket.id
  acl    = "private"
}

resource "aws_security_group" "emr_master" {
  name        = "${var.clusterName}-master-sg"
  description = "Security group for EMR master node"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.clusterName}-master-sg"
  }
}

resource "aws_security_group" "emr_slave" {
  name        = "${var.clusterName}-slave-sg"
  description = "Security group for EMR slave nodes"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.clusterName}-slave-sg"
  }
}

resource "aws_emr_cluster" "spark_cluster" {
  name          = var.clusterName
  release_label = var.releaseLabel
  applications  = var.applications

  log_uri = "s3://${aws_s3_bucket.emr_bucket.bucket}/logs/"

  service_role = aws_iam_role.emr_service_role.arn

  master_instance_group {
    instance_type = var.masterInstanceType
  }

  core_instance_group {
    instance_type  = var.coreInstanceType
    instance_count = var.coreInstanceCount
  }

  ec2_attributes {
    key_name                          = var.keyName
    subnet_id                         = var.subnetId
    emr_managed_master_security_group = aws_security_group.emr_master.id
    emr_managed_slave_security_group  = aws_security_group.emr_slave.id
    instance_profile                  = aws_iam_instance_profile.emr_instance_profile.arn
  }

  tags = {
    Name        = var.clusterName
    Description = var.description
    ManagedBy   = "Terraform"
    Source      = "Backstage Template"
  }

  step {
    name              = "Run Spark Job"
    action_on_failure = "CONTINUE"

    hadoop_jar_step {
      jar  = "command-runner.jar"
      args = ["spark-submit", "--deploy-mode", "cluster", var.sparkJobScript]
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.emr_service_role_policy_attachment,
    aws_iam_role_policy_attachment.emr_instance_profile_policy_attachment
  ]
}

# IAM roles and policies for EMR
resource "aws_iam_role" "emr_service_role" {
  name = "${var.clusterName}-emr-service-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "elasticmapreduce.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "emr_service_role_policy_attachment" {
  role       = aws_iam_role.emr_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceRole"
}

resource "aws_iam_role" "emr_instance_profile_role" {
  name = "${var.clusterName}-emr-instance-profile-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "emr_instance_profile_policy_attachment" {
  role       = aws_iam_role.emr_instance_profile_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforEC2Role"
}

resource "aws_iam_instance_profile" "emr_instance_profile" {
  name = "${var.clusterName}-emr-instance-profile"
  role = aws_iam_role.emr_instance_profile_role.name
} 