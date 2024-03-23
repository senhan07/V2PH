import undetected_chromedriver as uc

#! Initialize start the chrome engine
def run_engine():
    print("\nStarting chrome engine...")
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    # test_ua = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
    # options.add_argument(f'--user-agent={test_ua}')
    # options.add_argument("--headless")
    driver = uc.Chrome(options=options)
    driver.set_window_size(800, 600) 
    return driver
