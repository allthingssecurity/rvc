# cloudinary_upload.py
from boto3 import session
from botocore.client import Config
import os
ACCESS_ID = os.getenv('ACCESS_ID', 'default_value')
SECRET_KEY = os.getenv('SECRET_KEY', 'default_value')


def upload_to_do(file_path):
    # Configure Cloudinary with your credentials
    session = session.Session()
    client = session.client('s3',
                            region_name='nyc3',
                            endpoint_url='https://nyc3.digitaloceanspaces.com',
                            aws_access_key_id=ACCESS_ID,
                            aws_secret_access_key=SECRET_KEY)

    # Upload a file to your Space
    response=client.upload_file('c:/shashank/trips/test.mp3', 'sing', 'sing/test.mp3')

    
    return response
    
    



# Initiate session
