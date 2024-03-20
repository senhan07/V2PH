import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import os

# Start Chrome with undetected_chromedriver
options = uc.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
# options.add_argument("--enable-javascript")
driver = uc.Chrome(options=options)

driver.set_window_size(800, 600)

actor_name = "Jangjoo"
base_url = "https://www.v2ph.com"
target_url = f"https://www.v2ph.com/actor/{actor_name}"

# Function to extract URLs from a page
def extract_urls(driver):
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Find all <a> tags within elements with class "h6"
    a_tags = soup.select('.h6 a')
    # Extract the href attributes
    urls = [tag['href'] for tag in a_tags]
    return urls

# Open the initial URL
driver.get(target_url)

# Initialize a list to store all URLs
all_urls = []

page = 1
while True:
    # Wait for the page to fully load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "albums-list")))

    # Extract URLs from the current page and add them to the list
    current_urls = extract_urls(driver)
    all_urls.extend(current_urls)

    # Find the next page button and click it
    next_button = driver.find_elements(By.XPATH, '//a[contains(text(), "Next")]')

    print(f"Scraping page {page}")
    if next_button:
        next_button[0].click()
        page += 1
    else:
        print("Next button not found, end of the page")
        break  # If no next button found, break the loop

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

output = 'albums_url'
os.makedirs(output, exist_ok=True)
# Save the output to a file
file_name = f"{output}/{current_date}_{actor_name}.txt"
with open(file_name, "w") as file:
    for url in all_urls:
        file.write(f"{base_url}{url}\n")

print("Data saved to:", file_name)
print("Found: ", len(all_urls), "Album")
# Close the browser
driver.quit()
