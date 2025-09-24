import os
import boto3
from botocore.client import Config

# MinIO server configuration
MINIO_ENDPOINT = "http://localhost:9000"   # change to your MinIO endpoint
ACCESS_KEY = "minio"
SECRET_KEY = "minio"
BUCKET_NAME = "models"
PREFIX = "llama318b"  # S3 path prefix inside bucket
LOCAL_MODELS_DIR = "./models"  # folder containing model files

# Create S3 client
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1"  # MinIO defaults to this
)

# Walk through local models directory and upload files
for root, _, files in os.walk(LOCAL_MODELS_DIR):
    for filename in files:
        local_path = os.path.join(root, filename)

        # Compute S3 key with prefix, preserving relative folder structure
        relative_path = os.path.relpath(local_path, LOCAL_MODELS_DIR)
        s3_key = f"{PREFIX}/{relative_path}"

        print(f"Uploading {local_path} -> s3://{BUCKET_NAME}/{s3_key}")
        s3.upload_file(local_path, BUCKET_NAME, s3_key)
