from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
import random

chrome_options = ChromeOptions()

chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = Chrome(chrome_options=chrome_options)
driver.get("https://breached.to")
WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "forums__forum-name"))
)
elem = driver.find_elements(By.CLASS_NAME, "forums__forum-name")
for e in elem:
    print(e.get_attribute("href"))