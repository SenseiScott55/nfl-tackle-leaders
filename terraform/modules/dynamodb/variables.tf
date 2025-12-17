variable "table_name" {
  description = "Name of the DynamoDB table"
  type        = string
  default     = "nfl_weekly_leaders"

  validation {
    condition     = length(var.table_name) > 0 && length(var.table_name) <= 255
    error_message = "Table name must be between 1 and 255 characters."
  }
}

variable "enable_point_in_time_recovery" {
  description = "Enable point-in-time recovery for the table"
  type        = bool
  default     = false # Set to true for production

  validation {
    condition     = can(tobool(var.enable_point_in_time_recovery))
    error_message = "Must be a boolean value (true or false)."
  }
}

variable "tags" {
  description = "A map of tags to assign to the resources"
  type        = map(string)
  default     = {}
}