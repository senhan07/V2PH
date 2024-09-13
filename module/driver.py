from seleniumbase import Driver

def run_engine():
    print("\nStarting chrome engine...")

    # Initialize the driver instance
    driver = Driver(uc=True, headless=True,)
    return driver

def solve_turnstile(driver):
    driver.driver.uc_switch_to_frame("iframe")
    driver.driver.uc_click("span.mark")