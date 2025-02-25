# This system prompt is optimized for the Docker environment in this repository and
# specific tool combinations enabled.
# We encourage modifying this system prompt to ensure the model has context for the
# environment it is running in, and to provide any additional information that may be
# helpful for the task at hand.

import platform
from datetime import datetime

SYSTEM_PROMPT = f"""<SYSTEM_CAPABILITY>
- You are utilising an Linux OS using {platform.machine()} architecture with internet access.
- Do not install any applications; use `curl` instead of `wget`.
- When running Bash commands that generate large amounts of output, redirect the output to a temporary file and use `str_replace_editor` or:  grep -n -B <lines before> -A <lines after> <query> <filename> to inspect the results.
- When making function calls on your computer, they may take time to complete and return results. Where possible, try to batch multiple calls into a single request.
- If the Bash tool times out, restart it immediately.
- The current date is {datetime.today().strftime('%A, %B %-d, %Y')}.
</SYSTEM_CAPABILITY>

<IMPORTANT>
- The AWSCC resource schema is available at: [Terraform AWSCC Provider Docs](https://github.com/hashicorp/terraform-provider-awscc/blob/main/docs/resources/). For example, the schema for `accessanalyzer_analyzer` can be found [here](https://github.com/hashicorp/terraform-provider-awscc/blob/main/docs/resources/accessanalyzer_analyzer.md).
- You can find equivalent resource examples in CloudFormation at: [AWS CloudFormation Resource Reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html).
- Every AWSCC resource includes a top-level attribute `id` that serves as the resource identifier. If the CloudFormation resource schema also has a similarly named top-level attribute `id`, it is mapped to a new attribute named `<type>_id`. For example, `web_experience_id` for the `awscc_qbusiness_web_experience` resource.
- Provide a complete example, including any necessary supporting resources such as IAM roles, policies, or other dependencies.
- When creating supporting Terraform resources, use AWSCC provider resources whenever possible.
- Avoid hardcoding attribute values such as AWS regions or AWS account IDs whenever possible.
- Follow security best practices by granting the least privilege necessary when creating IAM policies.
- Be mindful of resources that take time to create, such as EKS clusters—it's better to provide them as input variables.
- Unless necessary, avoid setting explicit dependencies using `depends_on`.
- When creating a Lambda function with source code, always use the resource type `aws_lambda_function`.
- When adding tags in AWSCC, always use the following format:
  tags = [{{
    key   = "Modified By"
    value = "AWSCC"
  }}]
- Avoid using variables where possible; instead, explicitly define all required resources and attribute values.
</IMPORTANT>"""

USER_PROMPT_DELETE = """
Your objective is to clean up the previously timeout Terraform destroy

Your tasks in sequential order
* Use bash to locate the current directory.
* Use working directory: {working_directory}.
* Run `terraform init` to initialize it.
* Run `terraform destroy -no-color -compact-warnings -auto-approve` to clean up.
* If destroy failed, stop the remaining steps.

Finally, add a marker file called `deleted.marker` in the working directory to mark that clean up is completed.
"""

USER_PROMPT_UPDATE = """
Your objective is to fix the previously timeout Terraform apply

Your tasks in sequential order
* Use bash to locate the current directory.
* Use working directory: {working_directory}.
* Run `terraform init` to initialize it.
* Run `terraform apply -no-color -compact-warnings -auto-approve` to test.
* Fix any errors as needed.
* Run `terraform destroy --auto-approve` to clean up.
* Run `terraform fmt` to lint the config.
* Only if `terraform apply` runs successfully, add a marker file called `created.marker` in the working directory.
* Only if `terraform destroy` runs successfully, add a marker file called `deleted.marker` in the working directory.
"""

USER_PROMPT_REVIEW = """
Your objective is to review an example on how to use resource {resource_name} using AWSCC Terraform provider.
The initial example already exist and you need to review it.

Couple rules to follow:
- AWS standard resource usually started with prefix `aws_`
- AWSCC resource start with prefix `awscc_`
- Certain AWS standard resource does not have equivalent in AWSCC, such as the data source

Your tasks in sequential order:
* Use bash to locate the current directory.
* Navigate to working directory: {working_directory}.
* Use cat command to read the Terraform configuration (main.tf)
* Review each resources, think step by step and highlight AWS standard resource that can be converted to AWSCC resource
* Laid out the list of resources that you think can be replaced and it's equivalent AWSCC resource name
* Using wget, check if each resource is available in AWSCC Terraform registry. If resource is not available (error 404 not found), do not change it.
* Skip the remaining steps if you think the configuration already optimized.
* Backup the main.tf into main.bak
* Create a new main.tf with the revised configuration using the equivalent AWSCC resources
* Run `terraform init` to initialize it.
* Run `terraform validate` to check for schema validation.
* Fix any schema issues and re-run `terraform validate` again.
* Run `terraform apply -no-color -compact-warnings -auto-approve` to test.
* Fix any errors as needed.
* Run `terraform destroy --auto-approve` to clean up.
* Run `terraform fmt` to lint the config.
* Remove any unused datasources around region or account id from the terraform configuration.

Finally, add a marker file called `reviewed.marker` in the working directory to mark that review is completed.
"""

USER_PROMPT_CREATE = """
Your objective is to create example on how to use resource {resource_name} using AWSCC Terraform provider.

Couple rules to follow:
- The attribute `policy_document` is a map of string, please use json encode.
- Change any reference to AWS account by using data source aws_caller_identity.
- Change any reference to AWS region by using data source aws_region.
- Use data source for any policy document.

Your tasks in sequential order:
* Navigate to the working directory: {working_directory} using cd.
* Download the AWSCC schema for {resource_name} with curl into the working directory.
* Inspect the schema content using cat.
* Create a Terraform configuration (main.tf) for {resource_name} based on the schema and rules.
* Initialize Terraform: terraform init.
* Validate the configuration: terraform validate.
* Fix any schema issues and re-run terraform validate.
* Add any required dependencies for {resource_name}, such as IAM roles or policies.
* Review and remove any unnecessary resources.
* Apply the configuration: terraform apply -no-color -compact-warnings -auto-approve.
* Fix any errors as needed.
* Destroy the resources: terraform destroy --auto-approve.
* If terraform apply succeeds, create a marker file: created.marker.
* If terraform destroy succeeds, create a marker file: deleted.marker.

Finally run `terraform fmt` to lint the config.
"""

USER_PROMPT_CLEANER = """
Your objective is to clean up the main.tf file and make it ready for pull requests to AWSCC repository.

Couple rules to follow:
- Remove the `terraform` block, we dont need it for the example.
- Remove the `provider "aws"` and `provider "awscc"` block, we also dont need it for the example.
- Comments in general are fine, but review and trim as needed.

Your tasks in sequential order:
* Use bash to locate the current directory.
* Use working directory: {working_directory}.
* Clean up the main.tf file using the rules above.

Finally, add a marker file called `cleaned.marker` in the working directory to mark that clean up is completed.
"""

USER_PROMPT_SUMMARY = """
Your objective is to generate 1-2 sentence summary of the provided Terraform configuration for resource: {resource_name}.

Couple rules to follow:
- Summary should be max 2 sentence and must be related to resource {resource_name}
- Title should be short, active sentence and related to resource {resource_name}

Your tasks in sequential order:
* Use bash to locate the current directory.
* Use working directory: {working_directory}.
* Use cat to review the main.tf file
* Write the summary into file `summary.txt` with format below.

Format:

### {{ insert title here }}

{{ insert summary here }}

Here is couple example for your references:

Example 1:

### Organization Analyzer

To enable {{.Name}} at the organization level, modify example below to match your AWS organization configuration.

Example 2:

### ECR Repository with lifecycle policy

To create ECR Repository with lifecycle policy that expires untagged images older than 14 days:

End of example.

Finally, add a marker file called `summary.marker` in the working directory to mark that summary has been generated.
"""