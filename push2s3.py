import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def upload_folder_to_s3(local_folder_path, bucket_name, s3_prefix=''):
    """
    Uploads all files from a local folder to an S3 bucket,
    maintaining the folder structure within S3 if s3_prefix is used.

    Args:
        local_folder_path (str): The path to the local folder containing model files.
        bucket_name (str): The name of the S3 bucket.
        s3_prefix (str, optional): An optional prefix to add to the S3 object keys.
                                   This can be used to simulate folders within the bucket.
                                   Defaults to an empty string.
    """
    s3_client = boto3.client('s3')

    if not os.path.isdir(local_folder_path):
        print(f"Error: Local folder '{local_folder_path}' not found.")
        return

    for root, _, files in os.walk(local_folder_path):
        for file_name in files:
            local_file_path = os.path.join(root, file_name)
            # Construct the S3 key, maintaining relative path from local_folder_path
            relative_path = os.path.relpath(local_file_path, local_folder_path)
            s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/") # Ensure forward slashes for S3

            try:
                s3_client.upload_file(local_file_path, bucket_name, s3_key)
                print(f"Uploaded '{local_file_path}' to 's3://{bucket_name}/{s3_key}'")
            except FileNotFoundError:
                print(f"Error: Local file '{local_file_path}' not found during upload.")
            except NoCredentialsError:
                print("Error: AWS credentials not found. Please configure your AWS credentials.")
            except ClientError as e:
                print(f"Error uploading '{local_file_path}': {e}")

if __name__ == "__main__":
    LOCAL_MODELS_DIR = "path/to/your/model/folder"  # Replace with your local folder path
    S3_BUCKET_NAME = "your-s3-bucket-name"          # Replace with your S3 bucket name
    S3_FOLDER_PREFIX = "models/"                     # Optional: Prefix for objects in S3 (e.g., 'models/')

    upload_folder_to_s3(LOCAL_MODELS_DIR, S3_BUCKET_NAME, S3_FOLDER_PREFIX)