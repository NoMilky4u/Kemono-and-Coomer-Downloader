import os
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_data(api_url):
    """
    Fetch data from the given API URL and return the JSON response.
    """
    logging.info(f"Fetching data from API: {api_url}")
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")
        exit(1)

def download_file(file_url, output_file_path):
    """
    Download a file from the given URL and save it to the specified path.
    Handles duplicate file names by appending a counter.
    """
    logging.info(f"Downloading file from: {file_url}")
    try:
        response = requests.get(file_url, stream=True, timeout=10)
        response.raise_for_status()

        # Resolve duplicate file names
        original_path = output_file_path
        counter = 1
        while os.path.exists(output_file_path):
            base, ext = os.path.splitext(original_path)
            output_file_path = f"{base} ({counter}){ext}"
            counter += 1

        # Write file in chunks
        with open(output_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        
        logging.info(f"File saved successfully: {output_file_path}")
    except requests.RequestException as e:
        logging.error(f"Failed to download file: {file_url}. Error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while downloading: {e}")

def download_attachments(attachments, base_url, output_dir):
    """
    Download all attachments from a list of attachments.
    """
    if not attachments:
        logging.warning("No attachments to download.")
        return

    for attachment in attachments:
        file_name = attachment.get('name')
        file_path = attachment.get('path')
        if not file_name or not file_path:
            logging.warning(f"Skipping attachment due to missing data: {attachment}")
            continue

        file_url = f"{base_url}{file_path}"
        output_file_path = os.path.join(output_dir, file_name)
        download_file(file_url, output_file_path)

def process_post(post, base_url, output_dir):
    """
    Process a single post, downloading its attachments and file (if present).
    """
    attachments = post.get('attachments', [])
    file_data = post.get('file')

    download_attachments(attachments, base_url, output_dir)

    if file_data:
        file_name = file_data.get('name')
        file_path = file_data.get('path')
        if file_name and file_path:
            file_url = f"{base_url}{file_path}"
            output_file_path = os.path.join(output_dir, file_name)
            download_file(file_url, output_file_path)

def process_data(data, base_url, output_dir):
    """
    Determine whether the data is for a single post or a profile and process it.
    """
    if isinstance(data, dict) and 'post' in data:
        # Single post data
        logging.info("Processing a single post.")
        process_post(data['post'], base_url, output_dir)
    elif isinstance(data, list):
        # Profile data (list of posts)
        logging.info(f"Processing profile with {len(data)} posts.")
        for post in data:
            process_post(post, base_url, output_dir)
    else:
        logging.error("Unexpected data format received from the API.")
        exit(1)

def determine_api_url(input_url):
    """
    Determine the appropriate API URL and base URL based on the input URL.
    """
    if input_url.startswith("https://kemono.su/patreon/user/"):
        return input_url.replace("/patreon/", "/api/v1/patreon/"), "https://n4.kemono.su/data"
    elif input_url.startswith("https://coomer.su/onlyfans/user/"):
        return input_url.replace("/onlyfans/", "/api/v1/onlyfans/"), "https://n3.coomer.su/data/"
    elif input_url.startswith("https://coomer.su/fansly/user/"):
        return input_url.replace("/fansly/", "/api/v1/fansly/"), "https://n3.coomer.su/data/"
    else:
        logging.error("Invalid URL. Please enter a valid URL.")
        exit(1)

def main():
    """
    Main entry point for the script.
    """
    input_url = input("Please enter the URL: ").strip()
    api_url, base_url = determine_api_url(input_url)

    output_dir = "downloaded_images"
    os.makedirs(output_dir, exist_ok=True)

    data = fetch_data(api_url)
    process_data(data, base_url, output_dir)

    logging.info("All downloads completed successfully.")

if __name__ == "__main__":
    main()
