# IAM role for Lambda function
resource "aws_iam_role" "lambda_role" {
  name               = "${var.function_name}-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags = var.tags
}

# Assume role policy document
data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# CloudWatch Logs policy
resource "aws_iam_policy" "lambda_logging" {
  name        = "${var.function_name}-logging-policy"
  description = "IAM policy for logging from Lambda ${var.function_name}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })

  tags = var.tags
}

# Attach logging policy to role
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

# Attach additional policies (DynamoDB, etc.)
resource "aws_iam_role_policy_attachment" "additional_policies" {
  count      = length(var.attach_policy_arns)
  role       = aws_iam_role.lambda_role.name
  policy_arn = var.attach_policy_arns[count.index]
}

# VPC execution role (if VPC is used)
resource "aws_iam_role_policy_attachment" "lambda_vpc_execution" {
  count      = var.vpc_subnet_ids != null ? 1 : 0
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}