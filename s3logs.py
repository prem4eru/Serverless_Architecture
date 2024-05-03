import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Specify the S3 bucket name
    bucket_name = 'prembucketb4'

    # Connect to S3
    s3_client = boto3.client('s3')

    # List all the log files
    def list_log_files(bucket_name):
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='logs/')
        return [obj['Key'] for obj in response.get('Contents', [])]

    # Check the age of each log
    def is_old_log(log_key):
        last_modified = s3_client.head_object(Bucket=bucket_name, Key=log_key)['LastModified']
        age = datetime.now() - last_modified.replace(tzinfo=None)
        return age.days > 90

    # Delete logs older than 90 days
    def delete_old_logs(bucket_name):
        log_files = list_log_files(bucket_name)
        for log_file in log_files:
            if is_old_log(log_file):
                s3_client.delete_object(Bucket=bucket_name, Key=log_file)

    # Execute the function
    delete_old_logs(bucket_name)