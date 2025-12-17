variable "rule_name" {
  description = "Name of the EventBridge rule"
  type        = string
}

variable "description" {
  description = "Description of the EventBridge rule"
  type        = string
  default     = ""
}

variable "schedule_expression" {
  description = "Schedule expression (cron or rate)"
  type        = string
}

variable "enabled" {
  description = "Whether the rule is enabled"
  type        = bool
  default     = true
}

variable "target_lambda_arn" {
  description = "ARN of the Lambda function to trigger"
  type        = string
}

variable "target_lambda_name" {
  description = "Name of the Lambda function to trigger"
  type        = string
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}