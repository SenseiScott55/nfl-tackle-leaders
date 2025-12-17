# DynamoDB table for storing NFL weekly tackle and sack leaders
resource "aws_dynamodb_table" "nfl_leaders" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST" # On-demand pricing - perfect for low traffic

  # Composite primary key for efficient querying
  hash_key  = "PK"  # Partition key: SEASON#2025
  range_key = "SK"  # Sort key: WEEK#01#STAT#TOTAL_TACKLES

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

  # GSI for querying by stat type across all weeks
  attribute {
    name = "stat_type"
    type = "S"
  }

  attribute {
    name = "week_number"
    type = "N"
  }

  # Global Secondary Index - Query all weeks for a specific stat
  global_secondary_index {
    name            = "StatTypeIndex"
    hash_key        = "stat_type"
    range_key       = "week_number"
    projection_type = "ALL"
  }

  # Enable point-in-time recovery for data protection
  point_in_time_recovery {
    enabled = var.enable_point_in_time_recovery
  }

  # Server-side encryption
  server_side_encryption {
    enabled = true
  }

  # TTL disabled - we want to keep historical data
  ttl {
    enabled        = false
    attribute_name = ""
  }

  tags = merge(
    var.tags,
    {
      Name        = var.table_name
      Description = "NFL weekly leaders for tackles and sacks"
    }
  )
}

# IAM policy for Lambda functions to write to DynamoDB
resource "aws_iam_policy" "lambda_dynamodb_write" {
  name        = "${var.table_name}-lambda-write-policy"
  description = "Allow Lambda to write to ${var.table_name}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem"
        ]
        Resource = aws_dynamodb_table.nfl_leaders.arn
      }
    ]
  })

  tags = var.tags
}

# IAM policy for Lambda functions to read from DynamoDB
resource "aws_iam_policy" "lambda_dynamodb_read" {
  name        = "${var.table_name}-lambda-read-policy"
  description = "Allow Lambda to read from ${var.table_name}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          aws_dynamodb_table.nfl_leaders.arn,
          "${aws_dynamodb_table.nfl_leaders.arn}/index/*"
        ]
      }
    ]
  })

  tags = var.tags
}