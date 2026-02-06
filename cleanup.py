import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Find volumes with status 'available' (unattached)
    response = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    volumes = response['Volumes']

    if not volumes:
        print("No unattached volumes found.")
        return

    for vol in volumes:
        vol_id = vol['VolumeId']
        tags = vol.get('Tags', [])
        
        # Safety check: skip volumes tagged 'DoNotDelete'
        skip = any(tag['Key'] == 'DoNotDelete' and tag['Value'].lower() == 'true' for tag in tags)
        if skip:
            print(f"Skipping volume {vol_id} (tagged DoNotDelete).")
            continue

        try:
            ec2.delete_volume(VolumeId=vol_id)
            print(f"Deleted unattached volume: {vol_id}")
        except Exception as e:
            print(f"Error deleting {vol_id}: {e}")

if __name__ == "__main__":
    delete_unattached_volumes()

