variable "function_name" {
  description = "Name of the Lambda function"
  type        = string

  validation {
    condition     = length(var.function_name) > 0 && length(var.function_name) <= 64
    error_message = "Function name must be between 1 and 64 characters."
  }
}

variable "handler" {
  description = "Lambda function handler (e.g., 'handler.lambda_handler')"
  type        = string
  default     = "handler.lambda_handler"
}

variable "runtime" {
  description = "Lambda runtime (e.g., 'python3.11')"
  type        = string
  default     = "python3.11"
}

variable "timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 30

  validation {
    condition     = var.timeout >= 1 && var.timeout <= 900
    error_message = "Timeout must be between 1 and 900 seconds."
  }
}

variable "memory_size" {
  description = "Lambda function memory size in MB"
  type        = number
  default     = 256

  validation {
    condition     = var.memory_size >= 128 && var.memory_size <= 10240
    error_message = "Memory size must be between 128 and 10240 MB."
  }
}

variable "description" {
  description = "Description of the Lambda function"
  type        = string
  default     = ""
}

variable "environment_variables" {
  description = "Environment variables for the Lambda function"
  type        = map(string)
  default     = {}
}

variable "source_dir" {
  description = "Directory containing Lambda source code"
  type        = string
  default     = null
}

variable "zip_file" {
  description = "Path to pre-packaged Lambda zip file"
  type        = string
  default     = null
}

variable "create_package" {
  description = "Whether to create Lambda package from source_dir"
  type        = bool
  default     = true
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 7

  validation {
    condition = contains([
      1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180,
      365, 400, 545, 731, 1827, 3653
    ], var.log_retention_days)
    error_message = "Log retention must be a valid CloudWatch Logs retention value."
  }
}

variable "attach_policy_arns" {
  description = "List of IAM policy ARNs to attach to Lambda role"
  type        = list(string)
  default     = []
}

variable "vpc_subnet_ids" {
  description = "VPC subnet IDs for Lambda (optional)"
  type        = list(string)
  default     = null
}

variable "vpc_security_group_ids" {
  description = "VPC security group IDs for Lambda (optional)"
  type        = list(string)
  default     = null
}

variable "create_function_url" {
  description = "Create a Lambda function URL"
  type        = bool
  default     = false
}

variable "function_url_auth_type" {
  description = "Authorization type for function URL (NONE or AWS_IAM)"
  type        = string
  default     = "NONE"

  validation {
    condition     = contains(["NONE", "AWS_IAM"], var.function_url_auth_type)
    error_message = "Auth type must be NONE or AWS_IAM."
  }
}

# CORS configuration for function URL
variable "cors_allow_credentials" {
  description = "Whether to allow credentials in CORS"
  type        = bool
  default     = false
}

variable "cors_allow_origins" {
  description = "Allowed origins for CORS"
  type        = list(string)
  default     = ["*"]
}

variable "cors_allow_methods" {
  description = "Allowed methods for CORS"
  type        = list(string)
  default     = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
}

variable "cors_allow_headers" {
  description = "Allowed headers for CORS"
  type        = list(string)
  default     = ["*"]
}

variable "cors_expose_headers" {
  description = "Headers to expose in CORS"
  type        = list(string)
  default     = []
}

variable "cors_max_age" {
  description = "Max age for CORS preflight cache in seconds"
  type        = number
  default     = 3600
}

variable "tags" {
  description = "A map of tags to assign to resources"
  type        = map(string)
  default     = {}
}