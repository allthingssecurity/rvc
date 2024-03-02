import requests

def download_and_save_pth_file(url, model_name, save_path):
    """
    Downloads a .pth file from the given URL by sending a POST request with a model name
    and saves it to the specified local path.
    
    :param url: URL of the Flask endpoint.
    :param model_name: Name of the model to request the weights for.
    :param save_path: Local path to save the downloaded .pth file.
    """
    # Prepare the data payload as a dictionary
    data = {'model_name': model_name}

    # Send the POST request with JSON data
    response = requests.post(url, json=data, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Open a local file with write-binary mode and write the contents of the response
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192): 
                f.write(chunk)
        print(f"File downloaded and saved as: {save_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        print("Response:", response.text)

if __name__ == "__main__":
    # URL of the Flask endpoint that serves the .pth file
    url = "https://nbsq4wth0plslz-5000.proxy.runpod.net/get_weights"

    # Model name to request
    model_name = "cousin_brijesh"

    # Local path to save the downloaded .pth file
    save_path = "cousin_brijesh.pth"

    # Call the function to download and save the .pth file
    download_and_save_pth_file(url, model_name, save_path)
