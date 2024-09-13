from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import re
import glob
from module import driver
from module.login import login, logout, login_with_random_account
from module.history import visited_url, read_history
from module.driver import run_engine
from module.user import credentials, reset_token
from module.colors import CYAN, GREEN, RED, YELLOW, RESET
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate
from selenium.webdriver.common.by import By


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
    input = re.sub(r'\s+', ' ', input)
    return input

# Function to save URLs to a file with specified format

def save_urls_to_file(urls, selected_file, album_title):
    image_url = "image_url"
    os.makedirs(image_url, exist_ok=True)
    os.makedirs(os.path.join(image_url, selected_file), exist_ok=True)
    output_url = os.path.join(image_url, selected_file, f"{album_title}.txt")
    with open(output_url, 'w', encoding='utf-8') as file:
        for url, album_title in urls:
            if url:  # Check if URL is not empty
                normalize_album_title = normalize_alt_text(album_title)
                file.write(f"{url}\n    out={normalize_album_title}.jpg\n")
            else:
                pass  # Do nothing if URL is empty
    print(f"{GREEN}Data saved to:{RESET}", output_url)

def choose_album():
    print(f"{YELLOW}Select a files:{RESET}")
    album_url_folder = "albums_url"
    album_files = [f for f in os.listdir(album_url_folder) if f.endswith(".txt")]

    for i, file_name in enumerate(album_files):
        print(f"{i+1}. {file_name}")

    selected_option = input(f"{CYAN}Enter the number of the files (I to enter URL manually): {RESET}")

    if selected_option.upper() == 'I':
        manual_url = input(f"{CYAN}Enter the URL: {RESET}")
        return album_url_folder, manual_url, None
    
    selected_index = None
    while selected_index is None:
        try:
            selected_index = int(selected_option) - 1
            if selected_index < 0 or selected_index >= len(album_files):
                print(f"{RED}Invalid selection. Please enter a valid number.{RESET}")
                selected_option = input(f"{CYAN}Enter the number of the files (I to enter URL manually): {RESET}")
                if selected_option.upper() == 'I':
                    manual_url = input(f"{CYAN}Enter the URL: {RESET}")
                    return manual_url
                selected_index = None
        except ValueError:
            print(f"{RED}Invalid selection. Please enter a valid number.{RESET}")
            selected_option = input(f"{CYAN}Enter the number of the files (I to enter URL manually): {RESET}")
            if selected_option.upper() == 'I':
                manual_url = input(f"{CYAN}Enter the URL: {RESET}")
                return manual_url
    
    return album_url_folder, album_files, selected_index

def out_of_token(driver, username, successful_usernames, target_url):
    print(f"{RED}Out of token, switching to another account{RESET}")
    logout(driver)
    # Remove the username from successful_usernames to prevent logging in with it again
    successful_usernames.remove(username)
    username = login_with_random_account(driver)
    user_data = credentials(username)
    token = user_data.get("Token")
    login(driver, username)
    driver.get(target_url)

def print_output(rows):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
    # max_title_width = 100  # Define the maximum width for the title column
    headers = ["URL", "STATUS", "TITLE"]
    # formatted_rows = []
    # for url, title, status_msg in rows:
    #     # Truncate title if it exceeds the maximum width
    #     truncated_title = title[:max_title_width] + ('...' if len(title) > max_title_width else '')
    #     formatted_rows.append((url, truncated_title, status_msg))
    print(tabulate(rows, headers=headers, tablefmt="plain"))


def get_image(album_url_folder, album_files, selected_index):
    OUTOFTOKEN_URL = "https://www.v2ph.com/user/upgrade"
    driver = run_engine()
    
    if selected_index is not None:
        # Process the selected file
        selected_file = os.path.join(album_url_folder, album_files[selected_index])
        with open(selected_file, "r") as file:
            target_urls = file.readlines()
            history = read_history()
            username_to_urls = {}
            for username, urls in history.items():
                for url in urls:
                    username_to_urls[url] = username
            target_urls_stripped = [url.strip() for url in target_urls]
            # Sort target_urls based on usernames
            target_urls = sorted(target_urls_stripped, key=lambda url: username_to_urls.get(url, ''))
    else:
        # User entered the URL manually
        manual_url = album_files
        target_urls = [manual_url]

    successful_usernames = set()
    total_albums = len(target_urls)
    current_album = 1
    remaining_urls = []
    rows = []

    selected_filename = os.path.splitext(os.path.basename(selected_file))[0]
    # Check if the image_url folder is empty
    if not glob.glob(f"image_url/{selected_filename}/*.txt"):
        remaining_urls = target_urls
    else:
        print("Checking existing scrapped URLs...")
        # Iterate over target URLs
        remaining_urls = []
        for target_url in target_urls:
            target_url = target_url.strip()
            driver.get(target_url)
            pattern = re.compile(r"Page\s+not\s+found|404\s*-\s*Page\s+not\s+found|Error\s+404\s*:\s*Page\s+not\s+found")
            if pattern.search(driver.page_source):
                status_msg = f"{RED}Page Not Found{RESET}"
                title = None
                rows.append((target_url, status_msg, title))
                print_output(rows)
                total_albums -= 1
                continue
            # Wait for the title meta tag to be present
            title_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'meta[property="og:title"]'))
            )
            title = title_element.get_attribute('content')
            #  title = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:title"]').get_attribute('content')
            normalize_title = normalize_alt_text(title)
            if os.path.exists(f"image_url/{selected_filename}/{normalize_title}.txt"):
                status_msg = f"{YELLOW}Already scraped{RESET}"
                rows.append((target_url, status_msg, title))
                print_output(rows)
                # print(f"{normalize_title} already scraped. {YELLOW}Skipping...{RESET}")
                total_albums -= 1
            else:
                remaining_urls.append(target_url)
                status_msg = f"{CYAN}Added to queue{RESET}"
                rows.append((target_url, status_msg, title))
                print_output(rows)
        print(f"{GREEN}Checking completed{RESET}")
    #! Iterate over the remaining URLs
    while True:
        for target_url in remaining_urls:
            target_url = target_url.strip()
            unique_urls = set()
            reset_token()

            #! Add the album url already exists or not
            # username = check_history(target_url.strip())
            # user_data = credentials(username)
            # token = user_data.get("Token")

            if username in successful_usernames:
                pass
                # If the username has been used successfully before, skip the login process
                # print(f"{YELLOW}Skipping login with username {username} as it has been used successfully before.{RESET}")
            else:
                # If the username has not been used successfully before, attempt login
                logout(driver)
                username = login_with_random_account(driver)
                login(driver, username)
                if username:
                    successful_usernames.add(username)
            
            user_data = credentials(username)
            token = user_data.get("Token")

            driver.get(target_url)

            # Check if the account token has run out
            if driver.current_url == OUTOFTOKEN_URL:
                out_of_token(driver, username, successful_usernames, target_url)
                # print(f"{RED}Out of token, switching to another account{RESET}")
                # logout(driver)
                # # Remove the username from successful_usernames to prevent logging in with it again
                # successful_usernames.remove(username)
                # username = login_with_random_account(driver)
                # user_data = credentials(username)
                # token = user_data.get("Token")
                # login(driver, username)
                # driver.get(target_url)

            # Print progress status
            print(f"\n{YELLOW}Progress: ({current_album} of {total_albums}) albums{RESET}")

            current_album += 1
            all_urls = []
            page = 1

            #! Starting individual page scrapping
            while True:
                #! Check if the account token run out
                user_data = credentials(username)
                token = user_data.get("Token")
                if driver.current_url == OUTOFTOKEN_URL:
                    out_of_token(driver, username, successful_usernames, target_url)
                #     print(f"{RED}Out of token, switching to another account{RESET}")
                #     logout(driver)
                #     # Remove the username from successful_usernames to prevent logging in with it again
                #     successful_usernames.remove(username)
                #     username = login_with_random_account(driver)
                #     user_data = credentials(username)
                #     token = user_data.get("Token")
                #     login(driver, username)
                #     driver.get(target_url)

                visited_url(target_url, username)
                # Wait for the page to fully load
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "photos-list")))

                # Find the next page button and click it
                next_button = driver.find_elements(By.XPATH, '//a[contains(text(), "Next")]')
                
                if next_button:
                    title = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:title"]').get_attribute('content')
                    # Extract URLs from the current page and add them to the list
                    current_urls = extract_urls(driver)
                    all_urls.extend(current_urls)
                    pass
                else:
                    print(f"Album requires VIP Membership, {YELLOW}skipping{RESET}")
                    break

                print(f"Scraping page {page}: {[title]}, found {len(current_urls)} images")
                if next_button:
                    next_button[0].click()
                    next_button = driver.find_elements(By.XPATH, '//a[contains(text(), "Next")]')
                    if next_button:
                        pass
                    else:
                        print(f"End of the pages, {YELLOW}stop scrapping{RESET}")
                        break

                    # try:
                    #     alert_element = driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-primary[href="/user/upgrade"]')
                    #     # If the alert element is found, handle the alert
                    #     print(f"Some images requires VIP Membership, {YELLOW}stopping scrapping{RESET}")
                    #     break 
                    # except NoSuchElementException:
                    #     # If the alert element is not found within the specified timeout, proceed with the rest of the code
                    #     pass  # Do nothing and continue with the execution

                    #! Check if the account token run out
                    user_data = credentials(username)
                    token = user_data.get("Token")
                    if driver.current_url == OUTOFTOKEN_URL:
                        out_of_token(driver, username, successful_usernames, target_url)
                        # print(f"{RED}Out of token, switching to another account{RESET}")
                        # logout(driver)
                        # # Remove the username from successful_usernames to prevent logging in with it again
                        # successful_usernames.remove(username)
                        # username = login_with_random_account(driver)
                        # login(driver, username)   
                    else:
                        page += 1
                else:
                    print(f"{YELLOW}Next button not found, end of the page{RESET}")
                    break  # If no next button found, break the loop
            album_title = normalize_alt_text(title)

            # Add the URLs to the set for deduplication
            unique_urls.update(all_urls)
            total_images = len(unique_urls)
            
            print(f"{GREEN}Found:{RESET} {total_images} Images")
            # Save the unique URLs to a file
            save_urls_to_file(unique_urls, selected_filename, album_title)

        driver.quit()
        break