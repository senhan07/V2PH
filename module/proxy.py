import requests
import subprocess
import os
import time

# Function to fetch proxy list and test ping
def get_and_test_proxies():
    # Fetch proxy list from API
    proxy_api_url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&timeout=500&proxy_format=ipport&format=text"
    response = requests.get(proxy_api_url)
    if response.status_code == 200:
        proxies = response.text.split('\n')

        # Test each proxy for ping
        lowest_ping = float('inf')
        best_proxy = None
        for proxy in proxies:
            if proxy:
                proxy = "http://" + proxy.strip()
                try:
                    start_time = time.time()
                    requests.get("https://www.google.com", proxies={"http": proxy}, timeout=15)
                    ping = (time.time() - start_time) * 1000
                    if ping < lowest_ping:
                        lowest_ping = ping
                        best_proxy = proxy
                except Exception as e:
                    print(f"Failed to test proxy {proxy}: {e}")

        if best_proxy:
            print(f"Best proxy found: {best_proxy} with ping {lowest_ping:.2f} ms")
            return best_proxy
        else:
            print("No working proxy found.")
            return None
    else:
        print("Failed to fetch proxy list.")
        return None
# get_and_test_proxies()
