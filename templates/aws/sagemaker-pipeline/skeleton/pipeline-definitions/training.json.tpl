{
  "Version": "2020-12-01",
  "Metadata": {},
  "Parameters": [
    {
      "Name": "InputDataUrl",
      "Type": "String",
      "DefaultValue": "s3://sagemaker-{region}-<account-id>/data/training"
    },
    {
      "Name": "ModelName",
      "Type": "String",
      "DefaultValue": "${pipeline_name}-model"
    }
  ],
  "PipelineExperimentConfig": {
    "ExperimentName": "${pipeline_name}",
    "TrialName": "${pipeline_name}-trial"
  },
  "Steps": [
    {
      "Name": "TrainingStep",
      "Type": "Training",
      "Arguments": {
        "AlgorithmSpecification": {
          "TrainingImage": "{{{{AccountID}}}}.dkr.ecr.{region}.amazonaws.com/sagemaker-training-image:latest",
          "TrainingInputMode": "File"
        },
        "RoleArn": "${role_arn}",
        "ResourceConfig": {
          "InstanceType": "${instance_type}",
          "InstanceCount": 1,
          "VolumeSizeInGB": 30
        },
        "InputDataConfig": [
          {
            "ChannelName": "training",
            "DataSource": {
              "S3DataSource": {
                "S3Uri": "{{{{InputDataUrl}}}}",
                "S3DataType": "S3Prefix",
                "S3DataDistributionType": "FullyReplicated"
              }
            }
          }
        ],
        "OutputDataConfig": {
          "S3OutputPath": "s3://sagemaker-{region}-<account-id>/models/${pipeline_name}"
        },
        "StoppingCondition": {
          "MaxRuntimeInSeconds": 86400
        }
      }
    },
    {
      "Name": "CreateModelStep",
      "Type": "Model",
      "Arguments": {
        "ExecutionRoleArn": "${role_arn}",
        "ModelName": "{{{{ModelName}}}}",
        "PrimaryContainer": {
          "ModelDataUrl": "{{{{TrainingStep.ModelArtifacts.S3ModelArtifacts}}}}",
          "Image": "{{{{AccountID}}}}.dkr.ecr.{region}.amazonaws.com/sagemaker-inference-image:latest",
          "Environment": {}
        }
      }
    }
  ]
} 