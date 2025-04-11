provider "aws" {
  region = var.region
}

resource "aws_iam_role" "lambda_role" {
  name = "${var.functionName}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "lambda_basic" {
  name       = "${var.functionName}-basic-policy"
  roles      = [aws_iam_role.lambda_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "function" {
  function_name = var.functionName
  description   = var.description
  role          = aws_iam_role.lambda_role.arn
  handler       = var.handler
  runtime       = var.runtime
  memory_size   = var.memorySize
  timeout       = var.timeout

  filename      = "function.zip"
  source_code_hash = filebase64sha256("function.zip")

  tags = {
    Name        = var.functionName
    Description = var.description
    ManagedBy   = "Terraform"
    Source      = "Backstage Template"
  }
} 