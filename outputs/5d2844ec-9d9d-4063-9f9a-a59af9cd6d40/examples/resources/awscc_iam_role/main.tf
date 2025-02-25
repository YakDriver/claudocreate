# Example of IAM Role for Lambda with basic execution permission
resource "awscc_iam_role" "lambda_role" {
  role_name = "lambda-basic-execution"
  path      = "/service-role/"

  assume_role_policy_document = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  description = "IAM role for Lambda basic execution"

  policies = [
    {
      policy_name = "lambda-basic-execution"
      policy_document = jsonencode({
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
    }
  ]

  tags = [{
    key   = "Modified By"
    value = "AWSCC"
  }]
}
