from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import random
import os
import json
from module.update_token import update_token
import pyautogui

def login(driver):
    driver.get("https://www.v2ph.com/login")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

    # Get a list of JSON files in the accounts folder
    json_files = [f for f in os.listdir("accounts") if f.endswith(".json")]

    # Filter out JSON files where token value is 0
    json_files = [f for f in json_files if not json.load(open(os.path.join("accounts", f))).get("Token") == "0"]

    # Check if there are any JSON files left after filtering
    if len(json_files) > 0:
        # Choose a random JSON file
        random_json_file = random.choice(json_files)
        credentials_file = os.path.join("accounts", random_json_file)

        # Read credentials from the chosen JSON file
        with open(credentials_file, 'r') as file:
            credentials = json.load(file)
            if credentials:
                email = credentials.get("Email")
                password = credentials.get("Password")
                
                # Find input elements and fill them with credentials
                email_input = driver.find_element(By.ID, "email")
                email_input.send_keys(email)

                password_input = driver.find_element(By.ID, "password")
                password_input.send_keys(password)

                print("\nLoaded Credentials as:")
                print(f"Email: {email}")
                print(f"Password: {password}")
                
                # Wait for a while to see the result
                driver.implicitly_wait(5)

        print("\nSolve CAPTCHA first, Press any key to continue...")
        input()
        print("Trying to login...")

        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_button.click()

        driver.get("https://www.v2ph.com/user/index")
        if driver.current_url == "https://www.v2ph.com/user/index":
            print("Login successful!")
            update_token(driver, credentials, credentials_file)
        else:
            try:
                error_message = driver.find_element(By.CLASS_NAME, "errorMessage").text
                print(f"Login failed! Error: {error_message}")
            except NoSuchElementException:
                print("Login failed! Unable to retrieve error message.")

    else:
        print("Error: No more accounts with a token value greater than 0.")


def logout(driver):
    print("Trying to logout...")
    driver.get("https://www.v2ph.com/user/logout")
    if driver.current_url == "https://www.v2ph.com/login":
        print("Logout successful!")
    else:
        print("Logout error!")