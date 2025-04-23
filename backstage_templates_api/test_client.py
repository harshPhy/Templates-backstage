import json
import os
from template_plugin.clients.client_factory import ClientFactory
from template_plugin.models.template_models import TemplateTask
from template_plugin.config.config import load_config

# Load default configuration
config = load_config()

# Override auth token if needed
# config.backstage.auth_token = generate_token("user:development/guest")

# Create backstage client with the configuration
client = ClientFactory.create_client("backstage")


def list_templates():    
    """List available templates."""
    templates = client.list_templates()
    print(json.dumps(templates, indent=4))

def get_template():
    """Get a specific template."""
    template = client.get_template("terraform-aws-rds-postgres")
    print(json.dumps(template, indent=4))

def get_template_parameters():
    """Get template parameters."""
    parameters = client.get_template_parameters("terraform-aws-rds-postgres")
    print(json.dumps(parameters, indent=4))

def execute_template():
    """Execute a template with parameters."""
    template_parameters = {
        "name": "my-rds-db",
        "db_name": "mydatabase",
        "description": "A test RDS instance",
        "environment": "dev",
        "engine_version": "14.3",
        "instance_class": "db.t3.micro",
        "parameter_group_name": "default.postgres14",
        "allocated_storage": 20,
        "storage_type": "gp2",
        "username": "postgres",
        "backup_retention_period": 7,
        "multi_az": False,
        "publicly_accessible": False,
        "vpc_id": "vpc-example",
        "subnets": ["subnet-example1", "subnet-example2"],
        "security_groups": ["sg-example"],
        "region": "us-east-1",
        "useS3": True,
        "s3FolderPath": "templates/",
        "linkExpirationMinutes": 1440,
        "repoUrl": "github.com?owner=harshPhy&repo=aws-rds"
    }

    task = TemplateTask(
        template_name="terraform-aws-rds-postgres",
        parameters=template_parameters,
        dry_run=False
    )
    
    # Execute the template
    response = client.execute_template(task,
                s3_bucket="physarum-backstage-templates",
                aws_access_key=os.getenv("BACKSTAGE_AWS_ACCESS_KEY"),
                aws_secret_key=os.getenv("BACKSTAGE_AWS_SECRET_KEY"),
                aws_region=os.getenv("BACKSTAGE_AWS_REGION")
                )
    print(json.dumps(response, indent=4))
    # Convert response to dict for JSON serialization
    
    

# Run the example functions
if __name__ == "__main__":
    # print("Listing templates:")
    # list_templates()
    
    # print("\nGetting template details:")
    # get_template()
    
    # print("\nGetting template parameters:")
    # get_template_parameters()
    
    print("\nExecuting template:")
    execute_template() 