import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
from module.update_token import reset_token
from module.login import login
from scrape_album import scrape_album
from get_image import get_image

# driver.get("https://www.v2ph.com/login")

# Wait for the page to load
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

json_files = [f for f in os.listdir("accounts") if f.endswith(".json")]
for json_file in json_files:
    credentials_file = os.path.join("accounts", json_file)
    with open(credentials_file, 'r') as file:
        credentials = json.load(file)
        reset_token(credentials, credentials_file)

print("1. Scrapping album URLs based on Model Names")
print("2. Get Image URLs from album URLs .txt")
print("3. Download Images from URLs list using Aria2c")

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
