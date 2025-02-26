# This system prompt is optimized for the Docker environment in this repository and
# specific tool combinations enabled.
# We encourage modifying this system prompt to ensure the model has context for the
# environment it is running in, and to provide any additional information that may be
# helpful for the task at hand.

import platform
from datetime import datetime

SYSTEM_PROMPT = f"""<SYSTEM_CAPABILITY>
- You are using a Linux OS with a {platform.machine()} architecture and internet access.
- Do not install any applications; use `curl` instead of `wget`.
- When running Bash commands that generate large amounts of output, redirect the output to a temporary file and use `str_replace_editor` or:  grep -n -B <lines before> -A <lines after> <query> <filename> to inspect the results.
- When making function calls on your computer, they may take time to complete and return results. Where possible, try to batch multiple calls into a single request.
- If the Bash tool times out, restart it immediately.
- The current date is {datetime.today().strftime('%A, %B %-d, %Y')}.
</SYSTEM_CAPABILITY>

<IMPORTANT>
Your objective is to create Terraform documentation for the AWS provider, following a structured format.

Documentation Outline:
1. Header: Subcategory, layout, page title, and description.
2. Resource Name & Description: Overview of the resource.
3. Example Usage: A basic Terraform configuration.
4. Argument Reference: List of required and optional arguments.
5. Attribute Reference: List of resource attributes.
6. Timeouts: List of configurable timeouts.
7. Import: Instructions and examples for importing the resource.

Rules for Example Generation:
* The policy_document attribute is a map of strings; always use jsonencode.
* Replace any AWS account references with the aws_caller_identity data source.
* Replace any AWS region references with the aws_region data source.
* Always use a data source for policy documents.
* Avoid hardcoding AWS-specific values in examples.
* Follow security best practices by granting the least privilege necessary in IAM policies.
* Unless necessary, avoid setting explicit dependencies using depends_on.
* Use explicit values instead of variables in examples for clarity.

Guidelines for Extracting Information from AWS SDK for Go v2:
1. Locate AWS API References:
  - Use the [AWS SDK for Go v2 documentation](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2) to find details about AWS services and their API operations.
  - Each AWS service has a package, and within that package, client methods represent API operations.
2. Identify CRUD Operations for a Given Resource:
  - For a resource (e.g., aws_apptest_test_case), find its corresponding service (apptest).
  - Look for API methods that correspond to CRUD operations:
    - Create: Methods like CreateTestCase, using CreateTestCaseInput and returning CreateTestCaseOutput.
    - Read: Methods like GetTestCase, using GetTestCaseInput and returning GetTestCaseOutput.
    - Update: Methods like UpdateTestCase, using UpdateTestCaseInput and returning UpdateTestCaseOutput.
    - Delete: Methods like DeleteTestCase, using DeleteTestCaseInput and returning DeleteTestCaseOutput.
    - Note: Not all AWS resources support all four CRUD operations.
3. Recognize Variations in Naming:
  - AWS sometimes uses alternative terms for CRUD operations:
    Put, Add → Create
    Describe, Read, List → Get
    Modify → Update
    Remove → Delete
4. Map API Struct Fields to Terraform Documentation:
  - Input Struct Fields → Terraform Arguments:
    - Fields in CreateTestCaseInput become Terraform arguments.
    - Arguments can be required or optional.
    - Example: Name in CreateTestCaseInput is a required string argument.
  - Output Struct Fields → Terraform Attributes:
    - Fields in CreateTestCaseOutput become Terraform attributes (read-only).
    - Example: TestCaseId in CreateTestCaseOutput is an attribute, as AWS generates it.
5. Ensure Clear, Accurate Argument and Attribute Descriptions:
  - Use precise, concise descriptions.
  - Example: Instead of "This field specifies the test case name," use "Name of the test case."
6. Provide a Complete Terraform Example:
  - Include a valid Terraform configuration that defines the resource.
  - Ensure supporting resources (e.g., IAM roles, policies) are correctly configured.
</IMPORTANT>"""

USER_PROMPT_DELETE = """
Add a marker file called `deleted.marker` in the working directory.
"""

USER_PROMPT_UPDATE = """
Add a marker file called `updated.marker` in the working directory.
"""

USER_PROMPT_REVIEW = """
Add a marker file called `reviewed.marker` in the working directory.
"""

USER_PROMPT_CREATE = """
Generate Terraform documentation for {resource_name} using the AWS provider. Follow the outlined format and adhere to the rules for example generation. Use the AWS SDK for Go v2 to extract resource details, including available CRUD operations, input and output structures, and required attributes. The final documentation should be structured, complete, and consistent with Terraform's documentation style.

Tasks (Executed in Order):
1. Navigate to the working directory {working_directory} using cd.
2. Download the relevant AWS SDK for Go v2 documentation for {resource_name} using curl.
3. Inspect the CRUD operations/methods and input/output structs using cat.
4. Create a documentation file ({resource_name}.html.markdown) based on the findings.
5. If documentation creation succeeds, create a marker file (created.marker) in the working directory.

Format example for documentation for a resource called `aws_batch_job_queue`:

---
subcategory: "Batch"
layout: "aws"
page_title: "AWS: aws_batch_job_queue"
description: |-
  Provides a Batch Job Queue resource.
---

# Resource: aws_batch_job_queue

Provides a Batch Job Queue resource.

## Example Usage

### Basic Example

```terraform
resource "aws_batch_job_queue" "test_queue" {{
  name     = "tf-test-batch-job-queue"
  state    = "ENABLED"
  priority = 1

  compute_environment_order {{
    order               = 1
    compute_environment = aws_batch_compute_environment.test_environment_1.arn
  }}

  compute_environment_order {{
    order               = 2
    compute_environment = aws_batch_compute_environment.test_environment_2.arn
  }}
}}
```

## Argument Reference

This resource supports the following arguments:

* `name` - (Required) Name of the job queue.
* `compute_environment` - (Optional) Set of compute environments mapped to a job queue and their order relative to each other. The job scheduler uses this parameter to determine which compute environment runs a specific job. Compute environments must be in the VALID state before you can associate them with a job queue. You can associate up to three compute environments with a job queue.
* `job_state_time_limit_action` - (Optional) Job state time limit actions mapped to a job queue. Specifies an action that AWS Batch will take after the job has remained at the head of the queue in the specified state for longer than the specified time.
* `priority` - (Required) Priority of the job queue. Job queues with a higher priority are evaluated first when associated with the same compute environment.
* `scheduling_policy_arn` - (Optional) ARN of the fair share scheduling policy. If this parameter is specified, the job queue uses a fair share scheduling policy. If this parameter isn't specified, the job queue uses a first in, first out (FIFO) scheduling policy. After a job queue is created, you can replace but can't remove the fair share scheduling policy.
* `state` - (Required) State of the job queue. Must be one of: `ENABLED` or `DISABLED`
* `tags` - (Optional) Key-value map of resource tags. If configured with a provider [`default_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default_tags-configuration-block) present, tags with matching keys will overwrite those defined at the provider-level.

### compute_environment

* `compute_environment` - (Required) ARN of the compute environment.
* `order` - (Required) Order of the compute environment. Compute environments are tried in ascending order. For example, if two compute environments are associated with a job queue, the compute environment with a lower order integer value is tried for job placement first.

### job_state_time_limit_action

* `action` - (Required) Action to take when a job is at the head of the job queue in the specified state for the specified period of time. Valid values include `"CANCEL"`
* `max_time_seconds` - Approximate amount of time, in seconds, that must pass with the job in the specified state before the action is taken. Valid values include integers between `600` & `86400`
* `reason` - (Required) Reason to log for the action being taken.
* `state` - (Required) State of the job needed to trigger the action. Valid values include `"RUNNABLE"`.

## Attribute Reference

This resource exports the following attributes in addition to the arguments above:

* `arn` - ARN of the job queue.
* `tags_all` - Map of tags assigned to the resource, including those inherited from the provider [`default_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default_tags-configuration-block).

## Timeouts

[Configuration options](https://developer.hashicorp.com/terraform/language/resources/syntax#operation-timeouts):

- `create` - (Default `10m`)
- `update` - (Default `10m`)
- `delete` - (Default `10m`)

## Import

In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import Batch Job Queue using the `arn`. For example:

```terraform
import {{
  to = aws_batch_job_queue.test_queue
  id = "arn:aws:batch:us-east-1:123456789012:job-queue/sample"
}}
```

Using `terraform import`, import Batch Job Queue using the `arn`. For example:

```console
% terraform import aws_batch_job_queue.test_queue arn:aws:batch:us-east-1:123456789012:job-queue/sample
```

"""

USER_PROMPT_CLEANER = """
Add a marker file called `cleaned.marker` in the working directory.
"""

USER_PROMPT_SUMMARY = """
Add a marker file called `summary.marker` in the working directory.
"""
