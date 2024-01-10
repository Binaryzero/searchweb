import os
import random
import string

import requests
from bs4 import BeautifulSoup


def download_png_files(url, save_directory):
    # Check if the save directory exists, if not, create it
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Send a GET request to the provided URL
    response = requests.get(url)
    # If the request is successful (status code 200), proceed with parsing the content
    if response.status_code == 200:
        # Parse the content of the response with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        # Find all 'img' tags in the parsed HTML
        img_tags = soup.find_all("img")

        # For each 'img' tag, check if the 'src' attribute ends with '.png'
        for img in img_tags:
            img_url = img["src"]
            if img_url.endswith(".png"):
                # If it does, send a GET request to download the image
                response = requests.get(img_url)
                # If the image is successfully downloaded, save it to the save directory
                if response.status_code == 200:
                    # Generate a random file name
                    file_name = (
                        "".join(
                            random.choices(string.ascii_letters + string.digits, k=10)
                        )
                        + ".png"
                    )
                    # Create the full file path
                    file_path = os.path.join(save_directory, file_name)
                    # Open the file in write binary mode and write the content of the response to it
                    with open(file_path, "wb") as file:
                        file.write(response.content)
                    # Print a success message
                    print(f"File '{file_name}' saved successfully at {file_path}")
                else:
                    # If the image could not be downloaded, print a failure message
                    print(f"Failed to download file from {img_url}")
    else:
        # If the initial GET request was not successful, print a failure message
        print("Failed to access the URL")


# Example usage
url = "https://example.com/images/"
save_directory = "/path/to/save/directory"

# Call the function with the example URL and save directory
download_png_files(url, save_directory)
