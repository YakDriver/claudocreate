---
subcategory: "ARC Zonal Shift"
layout: "aws"
page_title: "AWS: aws_arczonalshift_practice_run_configuration"
description: |-
  Provides a practice run configuration resource for ARC (Amazon Route 53 Application Recovery Controller) Zonal Shift.
---

# Resource: aws_arczonalshift_practice_run_configuration

Provides a practice run configuration resource for ARC Zonal Shift. Practice runs start weekly zonal shifts for a resource to shift traffic away from an Availability Zone. This helps verify that your applications can handle the shift of traffic away from an Availability Zone during actual incidents.

## Example Usage

```terraform
data "aws_cloudwatch_metric_alarm" "monitoring" {
  alarm_name = "high-error-rate"
}

resource "aws_arczonalshift_practice_run_configuration" "example" {
  resource_identifier = "resource-123"

  outcome_alarms {
    alarm_name = data.aws_cloudwatch_metric_alarm.monitoring.alarm_name
    region     = data.aws_region.current.name
  }

  blocked_dates = ["2025-12-25"]

  blocked_windows {
    recurrence {
      interval = "WEEKLY"

      time_windows {
        days             = ["SATURDAY", "SUNDAY"]
        start_time_of_day = "08:00"
        duration_in_hours = 12
      }
    }
  }

  blocking_alarms {
    alarm_name = "application-health"
    region     = data.aws_region.current.name
  }
}

data "aws_region" "current" {}
```

## Argument Reference

The following arguments are supported:

* `resource_identifier` - (Required) The identifier of the resource that AWS shifts traffic for with zonal autoshift.
* `outcome_alarms` - (Required) Configuration block for the outcome alarm for practice runs. This is a required Amazon CloudWatch alarm that Route 53 ARC uses to evaluate whether practice runs are successful. See [Outcome Alarms](#outcome_alarms) below.
* `blocked_dates` - (Optional) List of dates when Route 53 ARC should not start practice runs for the resource. Dates must be in YYYY-MM-DD format.
* `blocked_windows` - (Optional) Configuration block for time windows when Route 53 ARC should not start practice runs for the resource. See [Blocked Windows](#blocked_windows) below.
* `blocking_alarms` - (Optional) Configuration block for Amazon CloudWatch alarms that can block zonal autoshift practice runs. See [Blocking Alarms](#blocking_alarms) below.

### outcome_alarms

The following arguments are supported:

* `alarm_name` - (Required) Name of the CloudWatch alarm.
* `region` - (Required) AWS Region where the alarm exists.

### blocked_windows

The following arguments are supported:

* `recurrence` - (Required) Configuration block for how often the blocked window repeats. See [Recurrence](#recurrence) below.

### recurrence

The following arguments are supported:

* `interval` - (Required) How often the blocked window repeats. Valid value: `WEEKLY`.
* `time_windows` - (Required) Configuration block for the days of the week and times when Route 53 ARC can't start practice runs. See [Time Windows](#time_windows) below.

### time_windows

The following arguments are supported:

* `days` - (Required) Days of the week when Route 53 ARC can't start practice runs. Valid values: `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`.
* `start_time_of_day` - (Required) Time of day when the blocked window starts, in 24-hour format (HH:MM).
* `duration_in_hours` - (Required) Duration of the blocked window in hours.

### blocking_alarms

The following arguments are supported:

* `alarm_name` - (Required) Name of the CloudWatch alarm.
* `region` - (Required) AWS Region where the alarm exists.

## Attribute Reference

This resource exports the following attributes in addition to the arguments above:

* `arn` - Amazon Resource Name (ARN) of the practice run configuration.
* `name` - Name of the resource.
* `zonal_autoshift_status` - Status of zonal autoshift for the resource.

## Import

In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import ARC Zonal Shift Practice Run Configuration using the resource identifier. For example:

```terraform
import {
  to = aws_arczonalshift_practice_run_configuration.example
  id = "resource-123"
}
```

Using `terraform import`, import ARC Zonal Shift Practice Run Configuration using the resource identifier. For example:

```console
% terraform import aws_arczonalshift_practice_run_configuration.example resource-123
```