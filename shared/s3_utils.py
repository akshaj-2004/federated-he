import boto3

def upload_to_s3(bucket, file_path, key):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket, key)

def download_from_s3(bucket, key, file_path):
    s3 = boto3.client('s3')
    s3.download_file(bucket, key, file_path)
