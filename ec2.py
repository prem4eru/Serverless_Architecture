import boto3

# Initialize the EC2 client
ec2 = boto3.client('ec2')

# Create instances
instances = ec2.run_instances(
    ImageId='ami-0cf2b4e024cdb6960',  # Replace with your AMI ID
    MinCount=1,
    MaxCount=2,
    InstanceType='t2.micro',  # Replace with your desired instance type
    KeyName='tm',  # Replace with your key pair name
    SecurityGroupIds=['sg-0ed28da5ff37a789d'],  # Replace with your security group ID(s)
)

# Get instance IDs
instance_ids = [instance['InstanceId'] for instance in instances['Instances']]

# Tag instances
for instance_id in instance_ids:
    if instance_id == instance_ids[0]:  # First instance is tagged as 'Auto-Stop'
        ec2.create_tags(
            Resources=[instance_id],
            Tags=[
                {'Key': 'Name', 'Value': 'Auto-Stop'}
            ]
        )
    else:  # Second instance is tagged as 'Auto-Start'
        ec2.create_tags(
            Resources=[instance_id],
            Tags=[
                {'Key': 'Name', 'Value': 'Auto-Start'}
            ]
        )
