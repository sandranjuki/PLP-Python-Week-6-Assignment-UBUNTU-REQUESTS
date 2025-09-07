import os
import requests
from urllib.parse import urlparse

def fetch_image():
    # Prompt the user for the image URL
    url = input("Enter the URL of the image: ").strip()

    # Directory to save images
    save_dir = "Fetched_Images"
    os.makedirs(save_dir, exist_ok=True)  # Create directory if it doesn't exist

    try:
        # Fetch image from the internet
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise HTTPError for bad status codes

        # Extract filename from URL, or create a generic one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:  # If no filename in the URL
            filename = "downloaded_image.jpg"

        save_path = os.path.join(save_dir, filename)

        # Save the image in binary mode
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"✅ Image successfully fetched and saved as: {save_path}")

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    fetch_image()
