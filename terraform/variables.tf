variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, prod, etc.)"
  type        = string
  default     = "prod"
}

variable "project_name" {
  description = "Project name for tagging"
  type        = string
  default     = "nfl-tackle-leaders"
}

variable "dynamodb_table_name" {
  description = "DynamoDB table name for NFL leaders"
  type        = string
  default     = "nfl_weekly_leaders"
}

variable "current_season" {
  description = "Current NFL season year"
  type        = string
  default     = "2025"
}

variable "espn_api_base_url" {
  description = "ESPN Core API base URL"
  type        = string
  default     = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl"
}

variable "ingest_lambda_timeout" {
  description = "Timeout for ingest Lambda function (seconds)"
  type        = number
  default     = 120
}

variable "ingest_lambda_memory" {
  description = "Memory for ingest Lambda function (MB)"
  type        = number
  default     = 512
}

variable "api_lambda_timeout" {
  description = "Timeout for API Lambda function (seconds)"
  type        = number
  default     = 30
}

variable "api_lambda_memory" {
  description = "Memory for API Lambda function (MB)"
  type        = number
  default     = 256
}

variable "schedule_expression" {
  description = "EventBridge schedule for Lambda (cron or rate)"
  type        = string
  default     = "cron(0 14 ? * TUE *)" # Every Tuesday at 2 PM UTC (9 AM EST)
}

variable "enable_eventbridge" {
  description = "Enable EventBridge scheduled trigger"
  type        = bool
  default     = true
}