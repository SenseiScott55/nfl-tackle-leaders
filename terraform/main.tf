# Terraform Backend Resources (S3 + DynamoDB for state locking)
module "terraform_backend" {
  source = "./modules/terraform_backend"

  state_bucket_name = "${var.project_name}-terraform-state"
  lock_table_name   = "${var.project_name}-terraform-locks"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Purpose     = "Terraform State Management"
  }
}

# Local values for reuse 
locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# DynamoDB Table for storing NFL leaders
module "dynamodb" {
  source = "./modules/dynamodb"

  table_name                    = var.dynamodb_table_name
  enable_point_in_time_recovery = false # Set to true for production backup

  tags = local.common_tags
}

# Ingest Lambda - Fetches data from ESPN API and stores in DynamoDB
module "ingest_lambda" {
  source = "./modules/lambda"

  function_name = "${var.project_name}-ingest"
  description   = "Fetches NFL tackle and sack leaders from ESPN API"
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"
  timeout       = var.ingest_lambda_timeout
  memory_size   = var.ingest_lambda_memory

  zip_file       = "${path.root}/../lambda/ingest/ingest.zip"
  create_package = false

  environment_variables = {
    TABLE_NAME        = module.dynamodb.table_name
    CURRENT_SEASON    = var.current_season
    ESPN_API_BASE_URL = var.espn_api_base_url
    LOG_LEVEL         = "INFO"
  }

  # Attach DynamoDB read and write permissions
  attach_policy_arns = [
    module.dynamodb.lambda_write_policy_arn,
    module.dynamodb.lambda_read_policy_arn
  ]

  log_retention_days = 7

  tags = local.common_tags
}

# API Lambda - Serves data from DynamoDB
module "api_lambda" {
  source = "./modules/lambda"

  function_name = "${var.project_name}-api"
  description   = "API for querying NFL tackle and sack leaders"
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"
  timeout       = var.api_lambda_timeout
  memory_size   = var.api_lambda_memory

  zip_file       = "${path.root}/../lambda/api/api.zip"
  create_package = false

  environment_variables = {
    TABLE_NAME     = module.dynamodb.table_name
    CURRENT_SEASON = var.current_season
    LOG_LEVEL      = "INFO"
  }

  # Attach DynamoDB read permissions
  attach_policy_arns = [
    module.dynamodb.lambda_read_policy_arn
  ]

  # NO Function URL - using API Gateway instead
  create_function_url = false

  log_retention_days = 7

  tags = local.common_tags
}

# API Gateway for the API Lambda
module "api_gateway" {
  source = "./modules/api_gateway"

  api_name             = "${var.project_name}-api"
  description          = "API Gateway for NFL Tackle Leaders"
  stage_name           = "prod"
  lambda_function_name = module.api_lambda.function_name
  lambda_invoke_arn    = module.api_lambda.invoke_arn

  tags = local.common_tags
}

# EventBridge rule to trigger Lambda weekly
module "eventbridge" {
  source = "./modules/eventbridge"

  rule_name           = "${var.project_name}-weekly-trigger"
  description         = "Triggers NFL data ingest every Tuesday after Monday Night Football"
  schedule_expression = var.schedule_expression
  enabled             = var.enable_eventbridge

  target_lambda_arn  = module.ingest_lambda.function_arn
  target_lambda_name = module.ingest_lambda.function_name

  tags = local.common_tags
}

# S3 Static Website
module "s3_website" {
  source = "./modules/s3_website"

  bucket_name     = "${var.project_name}-website"
  index_html_path = "${path.root}/../frontend/index.html"

  tags = local.common_tags
}