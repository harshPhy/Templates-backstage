# S3 Module

This module provides functionality for interacting with AWS S3, specifically for:

1. Downloading files from S3
2. Uploading files to S3
3. Generating pre-signed URLs
4. Extracting zip files from S3 archives

## Components

### S3Client

The `S3Client` class handles basic S3 operations:

- Downloading files from S3
- Uploading files to S3
- Generating pre-signed URLs
- Unzipping files

### S3Downloader

The `S3Downloader` class is specifically designed for downloading and extracting template results from the Backstage API. It:

- Waits for a task to complete
- Determines the correct S3 key for downloading
- Downloads the file from S3
- Extracts the contents from the zip file
- Deletes the original zip file

## Usage Example

```python
from template_plugin.s3 import S3Client, S3Downloader

# Create an S3 client
s3_client = S3Client(
    aws_access_key="YOUR_ACCESS_KEY",
    aws_secret_key="YOUR_SECRET_KEY",
    aws_region="us-east-1"
)

# Download and extract a file
s3_downloader = S3Downloader(
    s3_client=s3_client,
    task_id="task-123",
    task=template_task,
    s3_bucket="my-bucket",
    local_path="/path/to/extract",
    task_status_callback=get_task_status_function
)

success, output_path, error = s3_downloader.download_and_extract()
if success:
    print(f"Successfully extracted to {output_path}")
else:
    print(f"Error: {error}")
```
