import undetected_chromedriver as uc

#! Initialize start the chrome engine
def run_engine():
    print("\nStarting chrome engine...")
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = uc.Chrome(options=options)
    driver.set_window_size(800, 600) 
    return driver
