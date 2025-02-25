data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# Create the SQS queue first
resource "awscc_sqs_queue" "example" {
  queue_name = "terraform-awscc-queue-example"
  tags = [{
    key   = "Modified By"
    value = "AWSCC"
  }]
}

# Create queue policy data source
data "aws_iam_policy_document" "queue_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = [data.aws_caller_identity.current.account_id]
    }
    actions = [
      "SQS:SendMessage",
      "SQS:ReceiveMessage"
    ]
    resources = [awscc_sqs_queue.example.arn]
  }
}

# Attach the policy to the queue
resource "awscc_sqs_queue_inline_policy" "example" {
  queue           = awscc_sqs_queue.example.queue_url
  policy_document = data.aws_iam_policy_document.queue_policy.json
}