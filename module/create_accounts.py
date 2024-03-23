from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import random
import string
import os
import json
import time
from datetime import datetime
from selenium_recaptcha_solver import RecaptchaSolver
from module.colors import GREEN, RED, YELLOW, RESET

# Function to generate a random email address
def generate_email():
    domain = "gmail.com"  # You can change the domain as needed
    random_email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    return f"{random_email}@{domain}"

# Function to generate a random password
def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

# Function to generate a username based on the email address
def generate_username(email):
    username = email.split('@')[0]  # Take the part before the '@' symbol
    return username.replace('.', '').replace('+', '')

def create_account(driver):
    solver = RecaptchaSolver(driver=driver)
    # Open the signup page
    driver.get("https://www.v2ph.com/signup")

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

    print("Generating Credentials...")
    # Generate random email, password, and username
    random_email = generate_email()
    random_password = generate_password()
    random_username = generate_username(random_email)

    # Find input elements and fill them with generated values
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(random_email)

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(random_password)

    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(random_username)

    recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')

    retries = 0
    max_retries = 5
    while retries < max_retries:
        try:
            print(f"{YELLOW}Trying to Solving CAPTCHA... Attempt {retries + 1}/{max_retries}{RESET}")
            solver.click_recaptcha_v2(iframe=recaptcha_iframe)
            break  # Exit the loop if successful
        except Exception as e:
            print(f"{RED}Error solving CAPTCHA: {e}{RESET}")
            retries += 1
            if retries < max_retries:
                print("Retrying...")
                driver.get("https://www.v2ph.com/signup")  # Reload the signup page
            else:
                print(f"{RED}Maximum retries exceeded. Aborting.{RESET}")
                return

    # Wait for a while to see the result
    driver.implicitly_wait(5)

    time.sleep(1)
    signup_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign Up')]")
    signup_button.click()

    driver.get("https://www.v2ph.com/user/index")
    if driver.current_url == "https://www.v2ph.com/user/index":
        now = datetime.now()
        # dd/mm/YY H:M:S
        date_created = now.strftime("%d/%m/%Y %H:%M:%S")

        # Create a dictionary to store user information
        user_info = {
            "Email": random_email,
            "Password": random_password,
            "Username": random_username,
            "Date Created": date_created,
            "Last Accessed": date_created,
            "Token": "16"
        }

        # Create a folder for accounts if it doesn't exist
        accounts_folder = 'accounts'
        os.makedirs(accounts_folder, exist_ok=True)

        # Save user information to a JSON file named after their email address
        json_file_path = os.path.join(accounts_folder, f"{random_email.split('@')[0]}.json")
        with open(json_file_path, 'w') as json_file:
            json.dump(user_info, json_file, indent=4)
            print(f"{GREEN}Account successfuly created{RESET}")
            print(f"Email: {random_email}")
            print(f"Password: {random_password}")
            print(f"Username: {random_username}")
            print(f"Date Created: {date_created}")
    else:
        try:
            error_message = driver.find_element(By.CLASS_NAME, "errorMessage").text
            print(f"{RED}Sign Up failed! Error: {error_message}{RESET}")
        except NoSuchElementException:
            print(f"{RED}Sign Up failed! Unable to retrieve error message.{RESET}")
