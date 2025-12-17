resource "aws_cloudwatch_event_rule" "schedule" {
  name                = var.rule_name
  description         = var.description
  schedule_expression = var.schedule_expression
  state               = var.enabled ? "ENABLED" : "DISABLED"  # FIXED: Changed from is_enabled to state

  tags = var.tags
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule      = aws_cloudwatch_event_rule.schedule.name
  target_id = "lambda"
  arn       = var.target_lambda_arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = var.target_lambda_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule.arn
}