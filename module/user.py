from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from datetime import datetime
import json
import os
from module.colors import GREEN, RED, YELLOW, RESET

def update_token(driver, username):
    user_credentials = credentials(username)
    credentials_file = f"accounts/{username}.json"
    # Extract the value from <span class="text-danger">16</span>
    try:
        value_span = driver.find_element(By.CLASS_NAME, "text-danger")
        new_token = value_span.text.strip()  # Extract the text inside the span tag
        print(f"{GREEN}Token updated, Current Token: {new_token}{RESET}")

        # Update the token value in the JSON data
        user_credentials["Token"] = new_token

        # Update the "Last Accessed" field
        user_credentials["Last Accessed"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Write the updated JSON data back to the file
        with open(credentials_file, 'w') as file:
            json.dump(user_credentials, file, indent=4)
    except NoSuchElementException:
        print(f"{RED}Unable to find token element.{RESET}")


def reset_token():
    # Reset all accounts token to 16 if the last accessed more than 12 hours with current time
    json_files = [f for f in os.listdir("accounts") if f.endswith(".json")]
    for json_file in json_files:
        credentials_file = os.path.join("accounts", json_file)
        with open(credentials_file, 'r') as file:
            credentials = json.load(file)

    # Check if "Last Accessed" field exists and if it's more than 12 hours ago
    last_accessed_str = credentials.get("Last Accessed")
    if last_accessed_str:
        last_accessed = datetime.strptime(last_accessed_str, "%d/%m/%Y %H:%M:%S")
        current_time = datetime.now()
        time_difference = current_time - last_accessed

        # Reset token to 16 if last accessed more than 12 hours ago
        if time_difference.total_seconds() > 12 * 3600:
            credentials["Token"] = "16"
            
            # Update the "Last Accessed" field
            credentials["Last Accessed"] = current_time.strftime("%d/%m/%Y %H:%M:%S")

            # Write the updated JSON data back to the file
            with open(credentials_file, 'w') as file:
                json.dump(credentials, file, indent=4)
                print(f"{YELLOW}Token reseted to 16 as last accessed more than 12 hours ago.\n{RESET}")

#! Get user credentials information
def credentials(username):
    credentials_file = f"accounts\{username}.json"
    try:
        with open(credentials_file, 'r') as file:
            credentials = json.load(file)
    except FileNotFoundError:
        return {}
    return credentials

#! Return username list with at least 1 token
def check_available_accounts():
    # Get a list of JSON files in the accounts folder
    json_files = [f for f in os.listdir("accounts") if f.endswith(".json")]

    # Initialize an empty list to store username-token pairs
    username_token_pairs = []

    # Iterate through each JSON file
    for f in json_files:
        # Read credentials from the JSON file
        with open(os.path.join("accounts", f), 'r') as file:
            credentials = json.load(file)
            # Check if the token value is greater than 0
            token = credentials.get("Token", "0")
            if int(token) > 0:
                # Add the username and token value to the list as a tuple
                username = credentials.get("Username")
                if username:
                    username_token_pairs.append((username, int(token)))

    if not username_token_pairs:
        print(f"{RED}Error: No more accounts with a token value greater than 0.{RESET}")
    return username_token_pairs