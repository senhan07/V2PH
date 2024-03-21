import undetected_chromedriver as uc
import os
import json
from module.token import reset_token
from scrape_album import scrape_album
from get_image import get_image

# driver.get("https://www.v2ph.com/login")

# Wait for the page to load
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

#! Reset all accounts token to 16 if the last accessed more than 12 hours with current time
json_files = [f for f in os.listdir("accounts") if f.endswith(".json")]
for json_file in json_files:
    credentials_file = os.path.join("accounts", json_file)
    print(credentials_file)
    with open(credentials_file, 'r') as file:
        credentials = json.load(file)
        print(credentials)
        reset_token(credentials, credentials_file)

# TODO: MAKE THE CHROME ENGINE START AFTER FINISHING ALL THE INPUT CHOICE
#! Input choice
print("1. Scrapping album URLs based on Model Names")
print("2. Get Image URLs from album URLs .txt")

choice = input("Enter your choice: ")

if choice == "1":
    actor_name = input("Input the Girl Name: ")

    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = uc.Chrome(options=options)
    driver.set_window_size(800, 600) 

    scrape_album(driver, actor_name)
    
elif choice == "2":

    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = uc.Chrome(options=options)
    driver.set_window_size(800, 600) 

    get_image(driver)
else:
    print("Invalid choice.")


# Close the browser
driver.quit()
