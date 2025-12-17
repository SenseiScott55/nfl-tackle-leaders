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

  source_dir    = "${path.root}/../lambda/ingest"
  create_package = true

  environment_variables = {
    TABLE_NAME       = module.dynamodb.table_name
    CURRENT_SEASON   = var.current_season
    ESPN_API_BASE_URL = var.espn_api_base_url
    LOG_LEVEL        = "INFO"
  }

  # Attach DynamoDB write permissions
  attach_policy_arns = [
    module.dynamodb.lambda_write_policy_arn
  ]

  log_retention_days = 7

  tags = local.common_tags
}

# API Lambda - Serves data from DynamoDB via Function URL
module "api_lambda" {
  source = "./modules/lambda"

  function_name = "${var.project_name}-api"
  description   = "API for querying NFL tackle and sack leaders"
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"
  timeout       = var.api_lambda_timeout
  memory_size   = var.api_lambda_memory

  source_dir    = "${path.root}/../lambda/api"
  create_package = true

  environment_variables = {
    TABLE_NAME     = module.dynamodb.table_name
    CURRENT_SEASON = var.current_season
    LOG_LEVEL      = "INFO"
  }

  # Attach DynamoDB read permissions
  attach_policy_arns = [
    module.dynamodb.lambda_read_policy_arn
  ]

  # Enable Lambda Function URL for easy API access
  create_function_url    = true
  function_url_auth_type = "NONE"

  # CORS configuration for web access
  cors_allow_origins = ["*"]
  cors_allow_methods = ["GET", "OPTIONS"]
  cors_allow_headers = ["Content-Type"]

  log_retention_days = 7

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

# Note: S3 website module will be added in next phase
# Note: API Gateway module optional (using Lambda Function URL for now)