# DynamoDB outputs
output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = module.dynamodb.table_name
}

output "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table"
  value       = module.dynamodb.table_arn
}

# Ingest Lambda outputs
output "ingest_lambda_name" {
  description = "Name of the ingest Lambda function"
  value       = module.ingest_lambda.function_name
}

output "ingest_lambda_arn" {
  description = "ARN of the ingest Lambda function"
  value       = module.ingest_lambda.function_arn
}

output "ingest_lambda_log_group" {
  description = "CloudWatch log group for ingest Lambda"
  value       = module.ingest_lambda.log_group_name
}

# API Lambda outputs
output "api_lambda_name" {
  description = "Name of the API Lambda function"
  value       = module.api_lambda.function_name
}

output "api_lambda_arn" {
  description = "ARN of the API Lambda function"
  value       = module.api_lambda.function_arn
}

output "api_lambda_log_group" {
  description = "CloudWatch log group for API Lambda"
  value       = module.api_lambda.log_group_name
}

# API Gateway outputs
output "api_gateway_url" {
  description = "API Gateway URL for API access"
  value       = module.api_gateway.api_endpoint
}

output "api_gateway_id" {
  description = "ID of the API Gateway"
  value       = module.api_gateway.api_id
}

# EventBridge outputs
output "eventbridge_rule_name" {
  description = "Name of the EventBridge rule"
  value       = module.eventbridge.rule_name
}

output "eventbridge_rule_arn" {
  description = "ARN of the EventBridge rule"
  value       = module.eventbridge.rule_arn
}

# Quick reference outputs
output "quick_reference" {
  description = "Quick reference for accessing resources"
  value = {
    website_url          = module.s3_website.website_url
    api_url              = module.api_gateway.api_endpoint
    ingest_function_name = module.ingest_lambda.function_name
    table_name           = module.dynamodb.table_name
    schedule             = var.schedule_expression
  }
}

# S3 Website outputs
output "website_url" {
  description = "Public URL for the NFL Leaders website"
  value       = module.s3_website.website_url
}

output "website_bucket" {
  description = "S3 bucket name for the website"
  value       = module.s3_website.bucket_name
}

# Terraform Backend outputs
output "terraform_state_bucket" {
  description = "S3 bucket for Terraform state"
  value       = module.terraform_backend.state_bucket_name
}

output "terraform_lock_table" {
  description = "DynamoDB table for state locking"
  value       = module.terraform_backend.lock_table_name
}