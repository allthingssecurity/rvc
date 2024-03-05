# cloudinary_upload.py
from boto3 import session
from botocore.client import Config

import os
from boto3 import session
from botocore.client import Config

ACCESS_ID = os.getenv('ACCESS_ID', 'default_value')
SECRET_KEY = os.getenv('SECRET_KEY', 'default_value')


def upload_to_do(file_path,spk_id):
    # Configure Cloudinary with your credentials
    session = session.Session()
    client = session.client('s3',
                            region_name='nyc3',
                            endpoint_url='https://nyc3.digitaloceanspaces.com',
                            aws_access_key_id=ACCESS_ID,
                            aws_secret_access_key=SECRET_KEY)

    # Upload a file to your Space
    response=client.upload_file(file_path, spk_id, f'sing/{spk_id}.pth')

    
    return response
    
    



# Initiate session
