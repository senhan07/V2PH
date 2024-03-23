from math import log
from module.driver import run_engine
from module.create_accounts import create_account
from module.login import logout

driver = run_engine()

i = 1
while i < 50:
    create_account(driver)
    logout(driver)
    i += 1