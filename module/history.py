import json
from module.token import check_available_accounts

# Function to read user information from JSON file
def read_user_info(username):
    try:
        with open(f'accounts/{username}.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

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

# TODO: PREVENT ALBUMS URLS GOT ADDED TO HISTORY.JSON IF THE TOKEN IS 0
# Function to update history for a user with a visited URL
def update_history(url, username):
    history = read_history()
    user_info = read_user_info(username)
    if username in history:
        if url not in history[username]:
            history[username].append(url)
            print(f"{url} added to history on user {username}")
            user_info['Token'] = max(0, int(user_info.get('Token', 0)) - 1)
            write_user_info(username, user_info)
    else:
        history[username] = [url]
        user_info['Token'] = max(0, int(user_info.get('Token', 0)) - 1)
        print(f"{url} added to history on user {username}")
        write_user_info(username, user_info)
    write_history(history)

# # Example usage
# update_history("https://www.v2ph.com/album/123123.html", "test1231")
update_history("https://www.v2ph.com/album/te12343st.html", "123")
