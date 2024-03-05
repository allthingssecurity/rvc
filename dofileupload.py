from boto3 import session
from botocore.client import Config

ACCESS_ID = 'DO0026WEQUG4WF6WQNJ9'
SECRET_KEY = 'UG7kQicGgWmkfVmESWK889RxZG49UqV7vRfYUJDFFUo'

# Initiate session
session = session.Session()
client = session.client('s3',
                        region_name='nyc3',
                        endpoint_url='https://nyc3.digitaloceanspaces.com',
                        aws_access_key_id=ACCESS_ID,
                        aws_secret_access_key=SECRET_KEY)

# Upload a file to your Space
response=client.upload_file('c:/shashank/trips/_Daur(PagalWorld.com.cm).mp3', 'sing', 'sing/test.mp3')
print(response)