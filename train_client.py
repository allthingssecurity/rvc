import requests

def upload_files(url, model_name, file_paths):
    """
    Uploads multiple files to a specified URL.

    :param url: The URL of the Flask endpoint.
    :param model_name: The name of the model to process the files.
    :param file_paths: A list of file paths of the audio files to upload.
    """
    # Prepare the files in the correct format for uploading
    files = [('file', (open(file_path, 'rb'))) for file_path in file_paths]
    
    # Include any additional data as a dictionary
    data = {'model_name': model_name}

    # Send a POST request to the server
    response = requests.post(url, files=files, data=data)

    # Handle the response
    if response.status_code == 200:
        print("Files uploaded successfully.")
        print(response.json())  # Print server response
    else:
        print("Failed to upload files.")
        print(response.text)

if __name__ == "__main__":
    # URL of the Flask endpoint
    url = "https://8x1mfa4q76rg7l-5000.proxy.runpod.net/process_audio"

    # Model name (adjust as needed)
    model_name = "shashank"

    # List of audio file paths to upload
    file_paths = ["c:/shashank/trips/1.mp3"]

    # Make the API call to upload the files
    upload_files(url, model_name, file_paths)
