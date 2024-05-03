import boto3

def lambda_handler(event, context):
    # Initialize EC2 client
    ec2_client = boto3.client('ec2')
    
    # Get all instances with 'Auto-Stop' tag
    response_stop = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['Auto-Stop']}])
    instances_stop = [instance['InstanceId'] for reservation in response_stop['Reservations'] for instance in reservation['Instances']]
    
    # Stop instances with 'Auto-Stop' tag
    if instances_stop:
        ec2_client.stop_instances(InstanceIds=instances_stop)
        print(f"Instances with 'Auto-Stop' tag stopped: {instances_stop}")
    
    # Get all instances with 'Auto-Start' tag
    response_start = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['Auto-Start']}])
    instances_start = [instance['InstanceId'] for reservation in response_start['Reservations'] for instance in reservation['Instances']]
    
    # Start instances with 'Auto-Start' tag
    if instances_start:
        ec2_client.start_instances(InstanceIds=instances_start)
        print(f"Instances with 'Auto-Start' tag started: {instances_start}")
    
    # Delete instances with 'Auto-Stop' tag
    if instances_stop:
        ec2_client.terminate_instances(InstanceIds=instances_stop)
        print(f"Instances with 'Auto-Stop' tag terminated: {instances_stop}")
    
    # Delete instances with 'Auto-Start' tag
    if instances_start:
        ec2_client.terminate_instances(InstanceIds=instances_start)
        print(f"Instances with 'Auto-Start' tag terminated: {instances_start}")