import os
import requests
from urllib.parse import urlparse

def fetch_image(url, save_dir="Fetched_Images"):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        # Check if response is an image
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            print(f"❌ Skipping {url}, not an image.")
            return

        # Check file size limit (optional, e.g., 5MB)
        content_length = response.headers.get('Content-Length', None)
        if content_length and int(content_length) > 5_000_000:
            print(f"❌ Skipping {url}, file too large.")
            return

        # Extract filename or generate one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_image.jpg"
        
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)

        # Prevent duplicate filenames
        base_name, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(save_path):
            filename = f"{base_name}_{counter}{ext}"
            save_path = os.path.join(save_dir, filename)
            counter += 1

        # Save image
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"✅ Fetched and saved: {save_path}")

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error for {url}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error for {url}: {e}")
    except Exception as e:
        print(f"❌ Unexpected error for {url}: {e}")


if __name__ == "__main__":
    urls = input("Enter image URLs separated by commas: ").strip().split(',')
    urls = [url.strip() for url in urls if url.strip()]
    for url in urls:
        fetch_image(url)
