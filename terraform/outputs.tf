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

output "api_lambda_url" {
  description = "Lambda Function URL for API access"
  value       = module.api_lambda.function_url
}

output "api_lambda_log_group" {
  description = "CloudWatch log group for API Lambda"
  value       = module.api_lambda.log_group_name
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
    api_url              = module.api_lambda.function_url
    ingest_function_name = module.ingest_lambda.function_name
    table_name           = module.dynamodb.table_name
    schedule             = var.schedule_expression
  }
}