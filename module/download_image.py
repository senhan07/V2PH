import subprocess
import os

# Function to download images using aria2c
def download_images(output_dir, album_title, all_urls):
    print(f"Staring downloading {all_urls} Images")
    os.makedirs(output_dir, exist_ok=True)
    subprocess.run(["aria2c", "-i", f"urls/{album_title}.txt", "-j", "8", "--referer", "https://www.v2ph.com", "-d", output_dir])
