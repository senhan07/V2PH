
from lib2to3.pgen2 import driver
from math import log
from pdb import run
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
from module.login import login, logout, login_with_random_account
from module.download_image import download_images
from module.history import check_history, visited_url
from module.driver import run_engine

# Function to extract URLs from a page
def extract_urls(driver):
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Find the photos-list container
    photos_list = soup.find('div', class_='photos-list')
    # Find all img tags within the photos-list container
    img_tags = photos_list.find_all('img')
    # Extract the data-src and alt attributes
    urls = [(img['data-src'], img['alt']) for img in img_tags]
    return urls

# Function to normalize alt text for Windows system path
def normalize_alt_text(input):
    invalid_chars = '\\/:*?"<>|'
    for char in invalid_chars:
        input = input.replace(char, ' ')
    return input

# Function to save URLs to a file with specified format
def save_urls_to_file(urls, album_title):
    os.makedirs('image_urls', exist_ok=True)
    output_url = f"image_urls/{album_title}.txt"
    with open(output_url, 'w', encoding='utf-8') as file:
        for url, album_title in urls:
            file.write(f"{url}\n    out={album_title}.jpg\n")
    print("Data saved to:", output_url)

def choose_album():
        # List all files in the "albums_url" folder
    album_url_folder = "albums_url"
    album_files = [f for f in os.listdir(album_url_folder) if f.endswith(".txt")]

    # Prompt the user to choose a file
    print("\nSelect a files:")
    for i, file_name in enumerate(album_files):
        print(f"{i+1}. {file_name}")

    # Validate user input
    selected_index = None
    while selected_index is None:
        try:
            selected_index = int(input("Enter the number of the file: ")) - 1
            if selected_index < 0 or selected_index >= len(album_files):
                print("Invalid selection. Please enter a valid number.")
                selected_index = None
        except ValueError:
            print("Invalid input. Please enter a number.")
    return album_url_folder, album_files, selected_index


def get_image(album_url_folder, album_files, selected_index):
    driver = run_engine()
    
    # Initialize a set to store unique URLs
    unique_urls = set()

    # Process the selected file
    selected_file = os.path.join(album_url_folder, album_files[selected_index])
    with open(selected_file, "r") as file:
        target_urls = file.readlines()
        
        # Create a set to store usernames that have been used successfully
        successful_usernames = set()

        for target_url in target_urls:
            target_url = target_url.strip()

            # TODO: add ex. Progress (1/10) albums
            # Reset url set
            unique_urls = set()

            #! Add the album url already exists or not
            username = check_history(target_url.strip())

            while True:
                if username in successful_usernames:
                    # If the username has been used successfully before, skip the login process
                    print(f"Skipping login with username {username} as it has been used successfully before.")
                else:
                    # If the username has not been used successfully before, attempt login
                    login(driver, username)
                    if username:
                        # If login was successful, add the username to the set of successful usernames
                        successful_usernames.add(username)

                # Open the initial URL
                driver.get(target_url)

                # Check if the account token has run out
                if driver.current_url == "https://www.v2ph.com/user/upgrade":
                    print("Out of token, switching to another account")
                    logout(driver)
                    # Remove the username from successful_usernames to prevent logging in with it again
                    successful_usernames.remove(username)
                    username = login_with_random_account()
                else:
                    # Get the title for directory name
                    title = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:title"]').get_attribute('content')

                    break  # Exit the loop if token is valid

            # Get the title for directory name
            # title = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:title"]').get_attribute('content')
            
            # Initialize a list to store all URLs
            all_urls = []

            page = 1
            #! Starting individual page scrapping
            while True:
                while True:
                    #! Check if the account token run out
                    # Check if the account token has run out
                    if driver.current_url == "https://www.v2ph.com/user/upgrade":
                        print("Out of token, switching to another account")
                        logout(driver)
                        # Remove the username from successful_usernames to prevent logging in with it again
                        successful_usernames.remove(username)
                        username = login_with_random_account()
                    else:
                        # Get the title for directory name
                        # title = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:title"]').get_attribute('content')

                        break  # Exit the loop if token is valid

                visited_url(target_url, username)
                # Wait for the page to fully load
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "photos-list")))

                # Extract URLs from the current page and add them to the list
                current_urls = extract_urls(driver)
                all_urls.extend(current_urls)
                
                # Get the title for directory name
                # title = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:title"]').get_attribute('content')

                # Find the next page button and click it
                next_button = driver.find_elements(By.XPATH, '//a[contains(text(), "Next")]')

                print(f"SCRAPPING [PAGE {page}]: {target_url}")
                if next_button:
                    next_button[0].click()
                    page += 1
                else:
                    print("Next button not found, end of the page")
                    break  # If no next button found, break the loop

            album_title = normalize_alt_text(title)

            # Add the URLs to the set for deduplication
            unique_urls.update(all_urls)
            total_images = len(unique_urls)
            
            print(f"Found: {total_images} Images")
            # Save the unique URLs to a file
            save_urls_to_file(unique_urls, album_title)

            output_download = f'images/{album_title}'
            # Download images using aria2c
            download_images(output_download, album_title)

        # Quit the driver
    driver.quit()
