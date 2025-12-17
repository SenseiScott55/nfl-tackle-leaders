# Lambda Module

Reusable Terraform module for creating AWS Lambda functions with best practices.

## Features

- ✅ Automatic code packaging from source directory
- ✅ CloudWatch Logs with configurable retention
- ✅ IAM role with least-privilege permissions
- ✅ Support for additional IAM policy attachments
- ✅ Optional VPC configuration
- ✅ Optional Lambda Function URL with CORS
- ✅ Environment variables support
- ✅ JSON structured logging

## Usage

### Basic Lambda Function
```hcl
module "my_lambda" {
  source = "./modules/lambda"

  function_name = "my-function"
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"
  timeout       = 30
  memory_size   = 256

  source_dir = "${path.root}/../lambda/my-function"

  environment_variables = {
    TABLE_NAME = "my-table"
    LOG_LEVEL  = "INFO"
  }

  tags = {
    Environment = "production"
  }
}
```

### Lambda with DynamoDB Access
```hcl
module "ingest_lambda" {
  source = "./modules/lambda"

  function_name = "nfl-ingest"
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"
  timeout       = 120
  memory_size   = 512

  source_dir = "${path.root}/../lambda/ingest"

  environment_variables = {
    TABLE_NAME = module.dynamodb.table_name
  }

  # Attach DynamoDB write policy
  attach_policy_arns = [
    module.dynamodb.lambda_write_policy_arn
  ]

  tags = {
    Project = "nfl-tackle-leaders"
  }
}
```

### Lambda with Function URL
```hcl
module "api_lambda" {
  source = "./modules/lambda"

  function_name = "nfl-api"
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"

  source_dir = "${path.root}/../lambda/api"

  # Enable function URL
  create_function_url    = true
  function_url_auth_type = "NONE"

  # CORS configuration
  cors_allow_origins = ["https://example.com"]
  cors_allow_methods = ["GET", "POST"]

  attach_policy_arns = [
    module.dynamodb.lambda_read_policy_arn
  ]
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| function_name | Name of the Lambda function | string | - | yes |
| handler | Function handler | string | `handler.lambda_handler` | no |
| runtime | Lambda runtime | string | `python3.11` | no |
| timeout | Timeout in seconds (1-900) | number | 30 | no |
| memory_size | Memory in MB (128-10240) | number | 256 | no |
| source_dir | Source code directory | string | null | no |
| zip_file | Pre-packaged zip file path | string | null | no |
| environment_variables | Environment variables map | map(string) | {} | no |
| attach_policy_arns | Additional IAM policies | list(string) | [] | no |
| log_retention_days | Log retention in days | number | 7 | no |

## Outputs

| Name | Description |
|------|-------------|
| function_name | Lambda function name |
| function_arn | Lambda function ARN |
| invoke_arn | Invoke ARN (for API Gateway) |
| role_arn | Execution role ARN |
| log_group_name | CloudWatch log group name |
| function_url | Function URL (if created) |

## Notes

- Automatically creates CloudWatch log group
- Automatically zips source code from `source_dir`
- IAM role follows least-privilege principle
- Supports both inline source and pre-packaged zips
```

---

## ✅ All Lambda Module Files Created!

**File locations:**
```
terraform/modules/lambda/
├── main.tf       ✅
├── iam.tf        ✅
├── variables.tf  ✅
├── outputs.tf    ✅
└── README.md     ✅