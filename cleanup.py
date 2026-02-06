import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])['Volumes']
    
    for vol in volumes:
        vol_id = vol['VolumeId']
        try:
            ec2.delete_volume(VolumeId=vol_id)
            print(f"Deleted unattached volume: {vol_id}")
        except Exception as e:
            print(f"Error deleting {vol_id}: {e}")
