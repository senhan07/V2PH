import os
import json
from module.user import reset_token
from module.scrape_album import scrape_album
from module.get_image import get_image, choose_album
from module.driver import run_engine


#! Reset all accounts token to 16 if the last accessed more than 12 hours with current time
json_files = [f for f in os.listdir("accounts") if f.endswith(".json")]
for json_file in json_files:
    credentials_file = os.path.join("accounts", json_file)
    with open(credentials_file, 'r') as file:
        credentials = json.load(file)
        reset_token(credentials, credentials_file)

#! Input choice
print("1. Scrapping album URLs based on Model Names")
print("2. Get Image URLs from album URLs .txt")

choice = input("Enter your choice: ")

if choice == "1":
    actor_name = input("Input the Girl Name: ")
    driver = run_engine()
    scrape_album(driver, actor_name)
    
elif choice == "2":
    album_url_folder, \
    album_files, \
    selected_index = choose_album()
    get_image(album_url_folder, album_files, selected_index)
else:
    print("Invalid choice.")