import subprocess
import os

# Function to download images using aria2c
def download_images(output_dir, album_title):
    print(f"Starting downloading...")
    os.makedirs(output_dir, exist_ok=True)
    subprocess.run(["aria2c", "-i", f"image_urls/{album_title}.txt", "-j", "8", "--referer", "https://www.v2ph.com", "-d", output_dir])
