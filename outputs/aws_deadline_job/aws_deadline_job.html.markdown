---
subcategory: "Deadline"
layout: "aws"
page_title: "AWS: aws_deadline_job"
description: |-
  Provides a AWS Deadline Job resource.
---

# Resource: aws_deadline_job

Provides an AWS Deadline Job resource. AWS Deadline is a render farm management solution that allows you to manage and scale your render farm infrastructure.

## Example Usage

```terraform
resource "aws_deadline_job" "example" {
  name        = "example-render-job"
  pool        = "render_pool"
  group       = "render_group"
  priority    = 50
  
  job_settings {
    frames     = "1-100"
    chunk_size = 10
    plugin     = "3dsmax"
  }

  tags = {
    Environment = "production"
    Project     = "scene1"
  }
}
```

## Argument Reference

The following arguments are supported:

* `name` - (Required) The name of the Deadline job.
* `pool` - (Required) The name of the pool where the job will be submitted.
* `group` - (Required) The group name for the job.
* `priority` - (Optional) The priority of the job. Higher numbers mean higher priority. Defaults to 50.
* `job_settings` - (Required) Configuration block for job-specific settings. Detailed below.
* `tags` - (Optional) Key-value map of resource tags.

### job_settings Configuration Block

The `job_settings` configuration block supports the following arguments:

* `frames` - (Required) The frame range for the job (e.g., "1-100", "1-10,20-30", "1,3,5").
* `chunk_size` - (Optional) The number of frames to be rendered per task. Defaults to 1.
* `plugin` - (Required) The render plugin to use (e.g., "3dsmax", "maya", "nuke").

## Attribute Reference

In addition to all arguments above, the following attributes are exported:

* `id` - The unique identifier for the Deadline job.
* `status` - The current status of the job.
* `completion_percentage` - The percentage of completion for the job.
* `submitted_date` - The timestamp when the job was submitted.
* `tags_all` - A map of tags assigned to the resource, including those inherited from the provider [`default_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default_tags-configuration-block).

## Timeouts

[Configuration options](https://developer.hashicorp.com/terraform/language/resources/syntax#operation-timeouts):

* `create` - (Default `30m`)
* `update` - (Default `30m`)
* `delete` - (Default `30m`)

## Import

Deadline Jobs can be imported using the `id`, e.g.,

```
$ terraform import aws_deadline_job.example job-12345678
```