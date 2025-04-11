# AWS Spark Pipeline on EMR: ${{values.clusterName}}

${{values.description}}

This Terraform configuration creates an AWS EMR cluster for running Spark pipelines with the following properties:

- **Cluster Name**: ${{values.clusterName}}
- **Release Label**: ${{values.releaseLabel}}
- **Applications**: ${{values.applications}}
- **Master Instance Type**: ${{values.masterInstanceType}}
- **Core Instance Type**: ${{values.coreInstanceType}}
- **Core Instance Count**: ${{values.coreInstanceCount}}

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform installed (v1.0.0 or newer)
- S3 bucket for storing logs and data
- Spark job script available in S3

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

## Accessing the Cluster

You can access the EMR cluster in several ways:

### 1. SSH to the Master Node

```bash
ssh -i your-key.pem hadoop@[master-public-dns]
```

### 2. EMR Web Interfaces

- Spark UI: [master-public-dns]:18080
- YARN ResourceManager: [master-public-dns]:8088
- HDFS NameNode: [master-public-dns]:50070

### 3. Using AWS CLI

```bash
aws emr describe-cluster --cluster-id [cluster-id]
```

## Running Spark Jobs

You can submit Spark jobs to the cluster using:

### 1. Spark Submit from the Master Node

```bash
spark-submit --class org.example.YourSparkApp \
  --master yarn \
  --deploy-mode cluster \
  s3://path/to/your/application.jar \
  [parameters]
```

### 2. AWS EMR Step API

```bash
aws emr add-steps \
  --cluster-id [cluster-id] \
  --steps Type=Spark,Name="Spark Job",ActionOnFailure=CONTINUE,Args=[--class,org.example.YourSparkApp,s3://path/to/your/application.jar,parameter1,parameter2]
```

## Monitoring

Monitor your EMR cluster's performance metrics and logs in the EMR console:
[EMR Console](https://console.aws.amazon.com/elasticmapreduce/home)
