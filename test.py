# cloudinary_upload.py
from boto3 import session
from botocore.client import Config
import os
import boto3
from botocore.exceptions import ClientError


ACCESS_ID = os.getenv('ACCESS_ID', 'DO0026WEQUG4WF6WQNJ9')
SECRET_KEY = os.getenv('SECRET_KEY', 'UG7kQicGgWmkfVmESWK889RxZG49UqV7vRfYUJDFFUo')



def upload_to_do(file_path, spk_id):
    # Configure Cloudinary with your credentials
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='nyc3',
                            endpoint_url='https://nyc3.digitaloceanspaces.com',
                            aws_access_key_id=ACCESS_ID,
                            aws_secret_access_key=SECRET_KEY)
    bucket_name = 'sing'  # Your bucket name
    filename_only = os.path.basename(file_path)
    
    # Check if the bucket exists
        # Attempt to create the bucket
    try:
        client.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
        print(f"Bucket {bucket_name} exists and is accessible.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchBucket':
            print("Bucket does not exist. Attempting to create it...")
            # Code to create the bucket
        elif error_code == '403':
            print("Access Denied. Check your permissions.")
        else:
            print(f"Error: {e}")

    # Upload a file to your Space
    response = client.upload_file(file_path, bucket_name, filename_only)
    
    return response
    
    

upload_to_do("c:/shashank/trips/mamta.mp3","hell")

# Initiate session
