from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from datetime import datetime
import json

def update_token(driver, credentials, credentials_file):
    # Extract the value from <span class="text-danger">16</span>
    try:
        value_span = driver.find_element(By.CLASS_NAME, "text-danger")
        new_token = value_span.text.strip()  # Extract the text inside the span tag
        print(f"Current Token: {new_token}")

        # Update the token value in the JSON data
        credentials["Token"] = new_token

        # Update the "Last Accessed" field
        credentials["Last Accessed"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Write the updated JSON data back to the file
        with open(credentials_file, 'w') as file:
            json.dump(credentials, file, indent=4)
            print("Token and Last Accessed updated in the JSON file.")
    except NoSuchElementException:
        print("Unable to find token element.")

def reset_token(credentials, credentials_file):
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
                print("Token reseted to 16 as last accessed more than 12 hours ago.")