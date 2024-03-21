
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
from module.login import login
from module.download_image import download_images
from module.history import update_history

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
def save_urls_to_file(urls, filename):
    os.makedirs('image_urls', exist_ok=True)
    with open(f'image_urls/{filename}.txt', 'w') as file:
        for url, alt in urls:
            filename = normalize_alt_text(alt)
            file.write(f"{url}\n    out={filename}.jpg\n")

def choose_album():
        # List all files in the "albums_url" folder
    album_url_folder = "albums_url"
    album_files = [f for f in os.listdir(album_url_folder) if f.endswith(".txt")]

    # Prompt the user to choose a file
    print("\nSelect a file:")
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


def get_image(driver):
    # TODO: SEPERATE CHOOSING ALBUMS URL TO A FUCTION
    # TODO: ADD DEDUPLICATION WHEN GRABBED IMAGE URLS
    
    #! SELECT ALBUM URL FROM .TXT
    album_url_folder, \
    album_files, \
    selected_index = choose_album()

    username = login(driver)

    # Process the selected file
    selected_file = os.path.join(album_url_folder, album_files[selected_index])
    with open(selected_file, "r") as file:
        target_urls = file.readlines()
        for target_url in target_urls:
                    # Open the initial URL
                    driver.get(target_url.strip())

                    # Get the title for directory name
                    title = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:title"]').get_attribute('content')
                    
                    # Check if the URL is already in history, if not save it
                    update_history(target_url.strip(), username)

                    # Initialize a list to store all URLs
                    all_urls = []

                    page = 1
                    while True:
                        # Wait for the page to fully load
                        wait = WebDriverWait(driver, 10)
                        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "photos-list")))

                        # Extract URLs from the current page and add them to the list
                        current_urls = extract_urls(driver)
                        all_urls.extend(current_urls)

                        # Find the next page button and click it
                        next_button = driver.find_elements(By.XPATH, '//a[contains(text(), "Next")]')
                        print(all_urls)
                        print(f"Scraping page {page}")
                        if next_button:
                            next_button[0].click()
                            page += 1
                        else:
                            print("Next button not found, end of the page")
                            break  # If no next button found, break the loop

                    album_title = normalize_alt_text(title)
                    # Save the URLs to a file
                    save_urls_to_file(all_urls, album_title)

                    output_dir = f'images/{title}'

                    print("Data saved to:", output_dir)
                    print("Found:", len(all_urls), "Images")

                    # Download images using aria2c
                    download_images(output_dir, album_title, all_urls)

    # Quit the driver
    driver.quit()
