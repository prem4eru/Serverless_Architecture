import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Initialize S3 client
    s3_client = boto3.client('s3')
    
    # Specify the bucket name
    bucket_name = 'prembucketb4'
    
    # List objects in the specified bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    
    # Get current time
    current_time = datetime.now()
    
    if 'Contents' in response:
        for obj in response['Contents']:
            # Get the object's last modified time
            last_modified = obj['LastModified']
            
            # Calculate the difference in time
            time_difference = current_time - last_modified
            
            # If the object is older than 30 days, delete it
            if time_difference > timedelta(days=30):
                object_key = obj['Key']
                s3_client.delete_object(Bucket=bucket_name, Key=object_key)
                print(f"Deleted object: {object_key}")
