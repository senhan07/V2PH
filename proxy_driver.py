from module.driver import run_engine
import undetected_chromedriver as uc
from module.proxy import get_and_test_proxies
from fake_useragent import UserAgent

#! Initialize start the chrome engine
def run_engine():
    # proxy = get_and_test_proxies()
    proxy = "http://105.112.140.218:8080"
    referer = "https://www.v2ph.com"
    print("\nStarting chrome engine...")
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    # options.add_argument('--proxy-server=http://' + proxy_address)
    options.add_argument('--proxy-server='+proxy)
    options.add_argument(f'--referer={referer}')
    ua = UserAgent()
    ua = ua.random
    options.add_argument(f'--user-agent={ua}')
    driver = uc.Chrome(options=options)
    driver.set_window_size(800, 600) 
    print(proxy)
    print(referer)
    print(ua)
    return driver


driver = run_engine()

# Define the URL, referer, and proxy
url = "https://cdn.v2ph.com/photos/Lks1vRelJnINgqG3.jpg"



# Load the URL
driver.get(url)

# Keep the browser open until user input
input()

# Close the browser
driver.quit()