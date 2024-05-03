import boto3

def lambda_handler(event, context):
    # Initialize the EC2 client
    ec2_client = boto3.client('ec2')
    
    # Define the instance ID of the original EC2 instance
    instance_id = 'snap-054cf45a85d7428cc'
    
    # Get the most recent snapshot for the given instance
    snapshots = ec2_client.describe_snapshots(Filters=[{'Name': 'volume-id', 'Values': [instance_id]}])
    sorted_snapshots = sorted(snapshots['Snapshots'], key=lambda x: x['StartTime'], reverse=True)
    latest_snapshot = sorted_snapshots[0]['SnapshotId']
    
    # Create a new EC2 instance using the latest snapshot
    response = ec2_client.run_instances(
        ImageId='ami-0cf2b4e024cdb6960',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        SubnetId='subnet-b58e6ecd',
        SecurityGroupIds=['sg-5f506e1b'],
        KeyName='Prem',
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'SnapshotId': latest_snapshot,
                    'DeleteOnTermination': True,
                    'VolumeSize': 8,
                    'VolumeType': 'gp2'
                }
            },
        ]
    )
    
    # Optional: return instance ID of the newly created EC2 instance
    new_instance_id = response['Instances'][0]['InstanceId']
    return {
        'statusCode': 200,
        'body': new_instance_id
    }