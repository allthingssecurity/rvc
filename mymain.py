# main.py
from upload import upload_to_cloudinary

file_path = "c:/shashank/trips/test.mp3"
public_id = "testme"

# Call the function with the file path and public ID
response = upload_to_cloudinary(file_path, public_id)

print(response)
