import os
from tqdm import tqdm
import subprocess
from module.colors import GREEN, RED, YELLOW, RESET, CYAN

# Function to choose an album file
def choose_album():
    image_url_folder = "image_urls"

    # List all files in the "albums_url" folder
    image_url_files = [f for f in os.listdir(image_url_folder) if f.endswith(".txt")]

    # Display file list
    print(f"\n{YELLOW}Select a file to download:{RESET}")
    for i, file_name in enumerate(image_url_files):
        print(f"{i+1}. {file_name}")

    while True:
        choice = input(f"{CYAN}Enter the number of the file (A for all): {RESET}").strip()
        if choice.lower() == 'a':
            return [os.path.join(image_url_folder, file) for file in image_url_files]
        try:
            index = int(choice)
            if 1 <= index <= len(image_url_files):
                return os.path.join(image_url_folder, image_url_files[index - 1])
            else:
                print(f"{RED}Invalid selection. Please enter a valid number or 'A' for all.{RESET}")
        except ValueError:
            print(f"{RED}Invalid input. Please enter a number or 'A' for all.{RESET}")

# Function to download images using aria2c with tqdm progress bar
def download_images():
    # Choose an album file or files
    album_files = choose_album()

    if isinstance(album_files, list):  # If multiple files selected
        for album_file in album_files:
            download_single_album(album_file)
    else:
        download_single_album(album_files)

def download_single_album(album_file):
    # Get the album title from the file name
    album_title = os.path.splitext(os.path.basename(album_file))[0]

    # Output directory
    output_download = f'images/{album_title}'
    os.makedirs(output_download, exist_ok=True)

    # Count the total number of lines in the input file to set the total number of downloads for tqdm
    total_lines = sum(1 for line in open(album_file)) // 2


    # Set up tqdm progress bar with speed indicator and unit "image"
    with tqdm(total=total_lines, desc=f"{GREEN}[DOWNLOADING]{RESET} {YELLOW}{album_title}{RESET}", unit="image", dynamic_ncols=True) as pbar:
        # List to store URLs that encounter errors
        error_urls = []

        # Run aria2c command with subprocess
        process = subprocess.Popen(["aria2c", "-i", album_file, "-j", "12", "--retry-wait=15", "--max-tries=10", "--auto-file-renaming=false", "--referer", "https://www.v2ph.com", "-d", output_download], stdout=subprocess.PIPE, universal_newlines=True)

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
        #     You can choose to retry downloading these URLs or handle them in any other way

    pbar.close()