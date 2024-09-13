from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from module.user import update_token, check_available_accounts, credentials
from module.create_accounts import create_account
from module.colors import GREEN, RED, YELLOW, RESET
from selenium_recaptcha_solver import RecaptchaSolver


def login_with_random_account(driver):
    # Check available username with token at least 1
    all_username = check_available_accounts(driver)
    # Sort username_token_pairs based on token value (highest to lowest)
    all_username.sort(key=lambda x: x[1], reverse=True)

    if not all_username:
        print(f"{RED}Error: No more accounts with a token value greater than 0.{RESET}")
        username = create_account(driver)
        logout(driver)
        return username

    # Get credentials of the account with the highest token value
    username = all_username[0][0]
    return username

def insert_credentials(driver, username):
    user_data = credentials(username)
    email = user_data.get("Email")
    username = user_data.get("Username")
    password = user_data.get("Password")
    token = user_data.get("Token")

    time.sleep(1)
    # Find input elements and fill them with credentials
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(email)

    # For password, you might need to retrieve it from your backend or somewhere secure.
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)

    print(f"\nTrying Login as:")
    print(f"Email: {email}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Last Token: {token}")


def login(driver, username):
    # solver = RecaptchaSolver(driver=driver)

    if driver.current_url == "https://www.v2ph.com/login":
        pass
    else:
        driver.get("https://www.v2ph.com/login")
    
    wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
    wait.until(EC.presence_of_element_located((By.XPATH, "//body")))  # Wait until the body element is present

    insert_credentials(driver, username)

    # recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')

    # retries = 0
    # max_retries = 15
    # while retries < max_retries:
    #     try:
    #         print(f"{YELLOW}Trying to Solving CAPTCHA... Attempt {retries + 1}/{max_retries}{RESET}")
    #         time.sleep(1)
    #         solver.click_recaptcha_v2(iframe=recaptcha_iframe)
    #         break  # Exit the loop if successful
    #     except Exception as e:
    #         print(f"{RED}Error solving CAPTCHA: {e}{RESET}")
    #         retries += 1
    #         if retries < max_retries:
    #             print("Retrying...")
    #             driver.get("https://www.v2ph.com/login")  # Reload the signup page
    #             wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
    #             wait.until(EC.presence_of_element_located((By.XPATH, "//body")))  # Wait until the body element is present
    #             insert_credentials(driver, username)
    #             time.sleep(1)
    #             solver.click_recaptcha_v2(iframe=recaptcha_iframe)
    #         else:
    #             print(f"{RED}Maximum retries exceeded. Aborting.{RESET}")
    #             return

    # Wait for a while to see the result
    driver.implicitly_wait(5)

    print("Trying to login...")
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
    login_button.click()

    driver.get("https://www.v2ph.com/user/index")
    if driver.current_url == "https://www.v2ph.com/user/index":
        print(f"{GREEN}Login successful!{RESET}")
        # Update token only if login successful
        update_token(driver, username)
    else:
        try:
            error_message = driver.find_element(By.CLASS_NAME, "errorMessage").text
            print(f"{RED}Login failed! Error: {error_message}{RESET}")
        except NoSuchElementException:
            print(f"{RED}Login failed! Unable to retrieve error message.{RESET}")
    return username

def logout(driver):
    print("Trying to logout...")
    driver.get("https://www.v2ph.com/user/logout")
    if driver.current_url == "https://www.v2ph.com/login":
        print(f"{GREEN}Logout successful!{RESET}")
    else:
        print(f"{RED}Logout error!{RESET}")
