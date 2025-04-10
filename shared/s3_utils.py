import boto3

s3 = boto3.client('s3')

def upload_to_s3(bucket_name, local_file, s3_file):
    s3.upload_file(local_file, bucket_name, s3_file)

def download_from_s3(bucket_name, s3_file, local_file):
    s3.download_file(bucket_name, s3_file, local_file)
