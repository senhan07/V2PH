import subprocess
import os
from tqdm import tqdm

# ANSI escape codes for colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[33m'
RESET = '\033[0m'

# Function to download images using aria2c with tqdm progress bar
def download_images(output_download, album_title):
    os.makedirs(output_download, exist_ok=True)
    
    # Count the total number of lines in the input file to set the total number of downloads for tqdm
    total_lines = sum(1 for line in open(f"image_urls/{album_title}.txt")) // 2
    
    # Set up tqdm progress bar with speed indicator and unit "image"
    with tqdm(total=total_lines, desc=f"{GREEN}[DOWNLOADING]{RESET} {YELLOW}{album_title}{RESET}", unit="image", dynamic_ncols=True) as pbar:
        # List to store URLs that encounter errors
        error_urls = []
        
        # Run aria2c command with subprocess
        process = subprocess.Popen(["aria2c", "-i", f"image_urls/{album_title}.txt", "-j", "12", "--retry-wait=15", "--max-tries=10", "--auto-file-renaming=false", "--referer", "https://www.v2ph.com", "-d", output_download], stdout=subprocess.PIPE, universal_newlines=True)

        # Read stdout line by line
        for stdout_line in process.stdout:
            # Check if the line contains the "Download complete" status, indicating a successful download
            if "Download complete" in stdout_line:
                # Update tqdm progress bar only for successful downloads
                pbar.update(1)
            elif "ERROR" in stdout_line:
                # If error encountered, extract the URL from the error message and add it to error_urls list
                url = stdout_line.split("=")[-1].strip()  # Extract URL by removing the "URI=" prefix
                error_urls.append(url)
                print(f"{RED}[ERROR]{RESET} {url}")  # Print error message in red
                
        # If any URLs encountered errors, you can handle them here
        # if error_urls:
        #     print("\nHandling error URLs...")
            # You can choose to retry downloading these URLs or handle them in any other way
            
    pbar.close()
