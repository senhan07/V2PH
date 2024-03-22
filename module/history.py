import json
from module.user import credentials
from module.login import login, login_with_random_account
from module.driver import run_engine

# Function to write user information to JSON file
def write_user_info(username, user_info):
    with open(f'accounts/{username}.json', 'w') as file:
        json.dump(user_info, file, indent=4)

# Function to read history from JSON file
def read_history():
    try:
        with open('history/history.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to write history to JSON file
def write_history(history):
    with open('history/history.json', 'w') as file:
        json.dump(history, file, indent=4)
    
# Function to update history for a user with a visited URL
def visited_url(url, username):
    history = read_history()
    user_info = credentials(username)

    user_token = user_info.get('Token')
    if username in history:
        if url not in history[username]:
            history[username].append(url)
            print("New Album viewed, Token decreased by 1")
            print(f"{url} added to history on user {username}")
            user_info['Token'] = user_info['Token'] = str(max(0, int(user_token) - 1))
            write_user_info(username, user_info)
    else:
        history[username] = [url]
        user_info['Token'] = user_info['Token'] = str(max(0, int(user_token) - 1))
        print("New Album viewed, Token decreased by 1")
        print(f"{url} added to history on user {username}")
        write_user_info(username, user_info)
    write_history(history)


# Check if the url already exist on history
def check_history(url):
    history = read_history()
    
    # Iterate through each user's history
    for user, urls in history.items():
        if url in urls:
            # URL exists in history, return user credentials
            user_data = credentials(user)
            username = user_data.get("Username")
            print(f"{url} already viewed by {username}")
            return username
    
    # URL not found in history, perform login
    print(f"{url} not found on any accounts, trying to login with other account...")
    username = login_with_random_account()
    return username