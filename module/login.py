from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from module.user import update_token, check_available_accounts, credentials
from module.colors import GREEN, RED, YELLOW, RESET

def login_with_random_account():
    # Check available username with token at least 1
    all_username = check_available_accounts()
    # Sort username_token_pairs based on token value (highest to lowest)
    all_username.sort(key=lambda x: x[1], reverse=True)

    if not all_username:
        print(f"{RED}Error: No more accounts with a token value greater than 0.{RESET}")
        return

    # Get credentials of the account with the highest token value
    username = all_username[0][0]
    return username

def login(driver, username):
    driver.get("https://www.v2ph.com/login")

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

    # Wait for a while to see the result
    driver.implicitly_wait(5)

    print(f"\n{YELLOW}Solve CAPTCHA first, Press any key to continue...{RESET}")
    input()
    print("Trying to login...")

    time.sleep(1)
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
