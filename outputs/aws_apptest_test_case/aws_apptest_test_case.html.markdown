---
subcategory: "AppTest"
layout: "aws"
page_title: "AWS: aws_apptest_test_case"
description: |-
  Provides an AppTest Test Case resource.
---

# Resource: aws_apptest_test_case

Provides an AppTest Test Case resource. This allows you to manage test cases for your AWS applications through AppTest.

## Example Usage

### Basic Example

```terraform
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

data "aws_iam_policy_document" "test_case_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"

    principals {
      type        = "Service"
      identifiers = ["apptest.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "test_case_role" {
  name               = "apptest-test-case-role"
  assume_role_policy = data.aws_iam_policy_document.test_case_assume_role.json
}

resource "aws_apptest_test_case" "example" {
  name        = "example-test-case"
  description = "Example test case for application testing"
  
  execution_role_arn = aws_iam_role.test_case_role.arn
  
  configuration {
    test_type    = "API"
    timeout      = 3600
    environment  = "PRODUCTION"
    target_uri   = "https://api.example.com/test"
  }

  tags = {
    Environment = "production"
    Team        = "testing"
  }
}
```

## Argument Reference

The following arguments are required:

* `name` - (Required) The name of the test case.
* `execution_role_arn` - (Required) The Amazon Resource Name (ARN) of the IAM role that AppTest assumes to run the test case.

The following arguments are optional:

* `description` - (Optional) A description of the test case.
* `configuration` - (Optional) Configuration block for the test case. Detailed below.
* `tags` - (Optional) Key-value map of resource tags. If configured with a provider [`default_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default_tags-configuration-block) present, tags with matching keys will overwrite those defined at the provider-level.

### configuration

The `configuration` block supports the following arguments:

* `test_type` - (Required) The type of test. Valid values are `API`, `UI`, or `PERFORMANCE`.
* `timeout` - (Optional) The maximum time in seconds that the test case can run. Defaults to 3600.
* `environment` - (Optional) The environment where the test case runs. Valid values are `DEVELOPMENT`, `STAGING`, or `PRODUCTION`.
* `target_uri` - (Required) The URI of the target application to test.

## Attribute Reference

In addition to all arguments above, the following attributes are exported:

* `id` - The unique identifier of the test case.
* `arn` - The Amazon Resource Name (ARN) of the test case.
* `created_at` - The timestamp when the test case was created.
* `last_modified_at` - The timestamp when the test case was last modified.
* `tags_all` - A map of tags assigned to the resource, including those inherited from the provider [`default_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default_tags-configuration-block).

## Timeouts

[Configuration options](https://developer.hashicorp.com/terraform/language/resources/syntax#operation-timeouts):

* `create` - (Default `30m`)
* `update` - (Default `30m`)
* `delete` - (Default `30m`)

## Import

In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import AppTest Test Case using the test case ID. For example:

```terraform
import {
  to = aws_apptest_test_case.example
  id = "tc-12345678"
}
```

Using `terraform import`, import AppTest Test Case using the test case ID. For example:

```console
% terraform import aws_apptest_test_case.example tc-12345678
```