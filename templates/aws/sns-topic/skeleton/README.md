# AWS SNS Topic: ${{values.topicName}}

This Terraform configuration creates an AWS SNS (Simple Notification Service) topic with the following properties:

- **Topic Name**: ${{values.topicName}}
- **Display Name**: ${{values.displayName}}
- **FIFO Topic**: ${{values.fifoTopic}}

## Subscriptions

{{#if values.subscriptions.length}}
The following subscriptions will be created:

| Protocol | Endpoint |
| -------- | -------- |

{{#each values.subscriptions}}
| {{this.protocol}} | {{this.endpoint}} |
{{/each}}
{{else}}
No subscriptions are configured for this topic. You can add subscriptions later using the AWS Console or Terraform.
{{/if}}

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform installed (v1.0.0 or newer)

## Usage

1. Initialize Terraform:

   ```bash
   terraform init
   ```

2. Create a deployment plan:

   ```bash
   terraform plan
   ```

3. Apply the configuration:

   ```bash
   terraform apply
   ```

4. To destroy the resources when no longer needed:
   ```bash
   terraform destroy
   ```

## Publishing Messages

To publish a message to the SNS topic using AWS CLI:

```bash
aws sns publish \
  --topic-arn <topic-arn> \
  --message "Your message here" \
  --subject "Your subject here"
```

{{#if values.fifoTopic}}
For FIFO topics, you must include a message group ID:

```bash
aws sns publish \
  --topic-arn <topic-arn> \
  --message "Your message here" \
  --message-group-id "group123" \
  --message-deduplication-id "unique123"
```

{{/if}}
