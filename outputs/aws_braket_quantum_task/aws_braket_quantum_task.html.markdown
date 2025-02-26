---
subcategory: "Braket"
layout: "aws"
page_title: "AWS: aws_braket_quantum_task"
description: |-
  Provides a Braket Quantum Task resource.
---

# Resource: aws_braket_quantum_task

Provides a Braket Quantum Task resource. This resource allows you to create and manage quantum computing tasks in Amazon Braket.

## Example Usage

```terraform
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

resource "aws_braket_quantum_task" "example" {
  action         = jsonencode({
    "braketSchemaHeader": {
      "name": "braket.task_specification",
      "version": "1"
    },
    "deviceParameters": {
      "ionQ": {
        "shots": 100
      }
    },
    "ir": {
      "program": "H 0\nCNOT 0 1"
    },
    "nShots": 100
  })
  device_arn     = "arn:aws:braket:::device/ionq/ionQdevice"
  output_s3_bucket = "my-output-bucket"
  output_s3_key_prefix = "quantum-task-output/"
  shots          = 100

  tags = {
    Name = "example-quantum-task"
  }
}
```

## Argument Reference

The following arguments are supported:

* `action` - (Required) The action to be executed. Must be a JSON-encoded string containing the quantum task specification.
* `client_token` - (Optional) The client token associated with the request. SDK automatically generates this if not provided.
* `device_arn` - (Required) The ARN of the quantum device to run the task on.
* `device_parameters` - (Optional) Additional parameters specific to the quantum device. Must be a JSON-encoded string.
* `output_s3_bucket` - (Required) The S3 bucket where task results will be stored.
* `output_s3_key_prefix` - (Required) The key prefix for the S3 bucket where task results will be stored.
* `shots` - (Required) The number of shots (quantum circuit executions) to run.
* `tags` - (Optional) Key-value map of resource tags.

## Attribute Reference

In addition to all arguments above, the following attributes are exported:

* `arn` - ARN of the quantum task.
* `created_at` - Timestamp at which the task was created.
* `device_config` - The device configuration used to run the task.
* `ended_at` - Timestamp at which the task ended.
* `failure_reason` - The reason for the task failure, if applicable.
* `output_s3_directory` - The full S3 path where task results are stored.
* `status` - Current status of the task. Possible values: CANCELLED, COMPLETED, FAILED, QUEUED, RUNNING.
* `tags_all` - A map of tags assigned to the resource, including those inherited from the provider's default tags block.

## Timeouts

[Configuration options](https://developer.hashicorp.com/terraform/language/resources/syntax#operation-timeouts):

* `create` - (Default `30m`)
* `delete` - (Default `10m`)

## Import

Braket Quantum Task can be imported using the task ARN, e.g.,

```terraform
import {
  to = aws_braket_quantum_task.example
  id = "arn:aws:braket:us-west-2:123456789012:quantum-task/12345678-1234-1234-1234-123456789012"
}
```

Using `terraform import`, import Braket Quantum Task using the task ARN. For example:

```console
% terraform import aws_braket_quantum_task.example arn:aws:braket:us-west-2:123456789012:quantum-task/12345678-1234-1234-1234-123456789012
```