import os
import json

from flask import redirect
from module.download_image import download_images
from module.user import reset_token
from module.scrape_album import scrape_album
from module.get_image import get_image, choose_album
from module.driver import run_engine
from module.colors import GREEN, RED, YELLOW, RESET, CYAN

def print_banner():
    banner = """
    ______ _    _  _____ _  __     __      _____  _____  _    _ 
    |  ____| |  | |/ ____| |/ /     \ \    / |__ \|  __ \| |  | |
    | |__  | |  | | |    | ' /       \ \  / /   ) | |__) | |__| |
    |  __| | |  | | |    |  <         \ \/ /   / /|  ___/|  __  |
    | |    | |__| | |____| . \         \  /   / /_| |    | |  | |
    |_|     \____/ \_____|_|\_\         \/   |____|_|    |_|  |_|
    """
    print(banner)

while True:
    # Reset all accounts token to 16 if the last accessed more than 12 hours with current time
    json_files = [f for f in os.listdir("accounts") if f.endswith(".json")]
    for json_file in json_files:
        credentials_file = os.path.join("accounts", json_file)
        with open(credentials_file, 'r') as file:
            credentials = json.load(file)
            reset_token(credentials, credentials_file)

    # Print banner
    print_banner()

    # Input choice
    print("1. Scrapping album URLs based on Model Names")
    print("2. Get Image URLs from albums")
    print("3. Download images from URLs .txt")
    print(f"{RED}4. Exit{RESET}")

    choice = input(f"{CYAN}Enter your choice: {RESET}")

    if choice == "1":
        actor_name = input("Input the Girl Name: ")
        driver = run_engine()
        scrape_album(driver, actor_name)
    
    elif choice == "2":
        album_url_folder, \
        album_files, \
        selected_index = choose_album()
        get_image(album_url_folder, album_files, selected_index)
    
    elif choice == "3":
        download_images()
    
    elif choice == "4":
        print("Exiting...")
        break
    
    else:
        print("Invalid choice.")
