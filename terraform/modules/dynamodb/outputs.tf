output "table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.nfl_leaders.name
}

output "table_arn" {
  description = "ARN of the DynamoDB table"
  value       = aws_dynamodb_table.nfl_leaders.arn
}

output "table_id" {
  description = "ID of the DynamoDB table"
  value       = aws_dynamodb_table.nfl_leaders.id
}

output "table_stream_arn" {
  description = "ARN of the DynamoDB table stream"
  value       = aws_dynamodb_table.nfl_leaders.stream_arn
}

output "lambda_write_policy_arn" {
  description = "ARN of the IAM policy for Lambda write access"
  value       = aws_iam_policy.lambda_dynamodb_write.arn
}

output "lambda_read_policy_arn" {
  description = "ARN of the IAM policy for Lambda read access"
  value       = aws_iam_policy.lambda_dynamodb_read.arn
}

output "gsi_name" {
  description = "Name of the Global Secondary Index"
  value       = "StatTypeIndex"
}