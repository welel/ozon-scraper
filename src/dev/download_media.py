import os
import requests
import argparse
import json
import hashlib
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED

# Constants
NUM_THREADS = 5  # Number of threads to use for downloading
VIDEOS_DIR = 'videos'
IMAGES_DIR = 'images'
SHUTDOWN = False  # To handle graceful shutdown


def calculate_md5(content):
    """Returns the MD5 hash of the given content."""
    md5 = hashlib.md5()
    md5.update(content)
    return md5.hexdigest()


def generate_filename(url, content):
    """Generates a filename using MD5 hash of content and original extension."""
    original_extension = os.path.splitext(url)[-1]
    md5_hash = calculate_md5(content)
    return f"{md5_hash}{original_extension}"


def download_file(url, folder):
    """Downloads a file from a URL to a specified folder with MD5 as filename."""
    global SHUTDOWN
    if SHUTDOWN:
        return
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        content = response.content
        filename = generate_filename(url, content)
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as file:
            file.write(content)
        print(f"Downloaded {filename} to {folder}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}. Error: {e}")


def process_images(data, executor):
    """Processes image URLs and downloads them."""
    os.makedirs(IMAGES_DIR, exist_ok=True)
    tasks = []
    for item in data:
        image_url = item.get('image_url')
        if image_url:
            modified_image_url = image_url.replace('wc50', 'wc500')
            task = executor.submit(download_file, modified_image_url, IMAGES_DIR)
            tasks.append(task)
    wait(tasks, return_when=ALL_COMPLETED)  # Wait for all tasks to complete


def process_videos(data, executor):
    """Processes video URLs and downloads them."""
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    tasks = []
    for item in data:
        video_url = item.get('video_url')
        if video_url:
            task = executor.submit(download_file, video_url, VIDEOS_DIR)
            tasks.append(task)
    wait(tasks, return_when=ALL_COMPLETED)  # Wait for all tasks to complete


def process_json(file_path):
    """Processes the JSON file to download videos and images."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Using ThreadPoolExecutor to manage threads
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            process_images(data, executor)  # Process images first
            process_videos(data, executor)  # Process videos next
            
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON file: {file_path}. Error: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {file_path}. Error: {e}")
    except KeyboardInterrupt:
        print("\nProcess interrupted. Canceling tasks...")
        global SHUTDOWN
        SHUTDOWN = True
        executor.shutdown(wait=False, cancel_futures=True)


def signal_handler(signum, frame):
    """Handles graceful shutdown on Ctrl+C."""
    global SHUTDOWN
    print("\nGraceful shutdown initiated...")
    SHUTDOWN = True


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Download videos and images from a JSON file."
    )
    parser.add_argument(
        'file_path', type=str,
        help="Path to the JSON file containing URLs."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Handle Ctrl+C for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Process the JSON file
    process_json(args.file_path)


if __name__ == "__main__":
    main()
