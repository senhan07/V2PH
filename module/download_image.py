import os
from tqdm import tqdm
import subprocess
from module.colors import GREEN, RED, YELLOW, RESET, CYAN

def choose_album(current_folder="image_url"):
    current_path = current_folder
    all_files = []
    all_folders = []
    
    # List files and folders in the current directory
    for item in os.listdir(current_path):
        full_path = os.path.join(current_path, item)
        if os.path.isfile(full_path) and item.endswith(".txt"):
            all_files.append(full_path)
        elif os.path.isdir(full_path):
            all_folders.append(full_path)
    
    # Display files and folders
    print(f"\n{YELLOW}Current Folder: {current_path}{RESET}")
    print(f"\n{YELLOW}Select a file or folder to explore, or 'A' to select all files:{RESET}")
    print(f"{CYAN}0. Go back{RESET}")
    for i, folder in enumerate(all_folders):
        print(f"{i + 1}. {os.path.basename(folder)} (Folder)")
    for j, file in enumerate(all_files):
        print(f"{j + len(all_folders) + 1}. {os.path.basename(file)} (File)")

    while True:
        choice = input(f"{CYAN}Enter the number of the file or folder, or 'A' to select all: {RESET}").strip()
        if choice.lower() == 'a':
            return all_files
        elif choice == '0':
            parent_folder = os.path.dirname(current_path)
            if parent_folder != current_path:
                return choose_album(parent_folder)
            else:
                print(f"{RED}You are already in the root folder.{RESET}")
        try:
            index = int(choice)
            if 1 <= index <= len(all_folders):
                return choose_album(all_folders[index - 1])
            elif len(all_folders) < index <= len(all_folders) + len(all_files):
                return [all_files[index - len(all_folders) - 1]]
            else:
                print(f"{RED}Invalid selection. Please enter a valid number, 'A' to select all, or '0' to go back.{RESET}")
        except ValueError:
            print(f"{RED}Invalid input. Please enter a number, 'A' to select all, or '0' to go back.{RESET}")

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