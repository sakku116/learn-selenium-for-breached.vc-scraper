from concurrent.futures import thread
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
# from selenium import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
import random
from bs4 import BeautifulSoup
import time

chrome_options = ChromeOptions()

# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument("start-maximized")
# chrome_options.add_argument("disable-infobars")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_experimental_option("detach", True)
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = Chrome(chrome_options=chrome_options)

url = driver.command_executor._url
session_id = driver.session_id

driver = webdriver.Remote(command_executor=url,desired_capabilities={})
driver.close()   # this prevents the dummy browser
driver.session_id = session_id

driver.get("https://breached.to")

time.sleep(30)

home_page = driver.page_source

WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "forums__forum-name"))
)
links = driver.find_elements(By.CLASS_NAME, "forums__forum-name")

# home_links = []
# for link in links:
#     link = link.get_attribute("href")
#     if "Leaks" not in link or "General" not in link:
#         home_links.append(link)

# print(home_links)


soup = BeautifulSoup(home_page, "html.parser")
results = []

trs = soup.find_all("tr")
for tr in trs:
    forum_name_elm = tr.find("a", class_="forums__forum-name")
    forum_desc_elm = tr.find("div", class_="forums__forum-description")
    forums_stats_elm = tr.find("td", class_="forums__stats")
    if forums_stats_elm:
        forums_stats_sibling_elm = forums_stats_elm.find_next_sibling("td", class_="forums__stats") # look for td.forums__stats's sibling

    if forum_name_elm:
        payload = {}
        payload["forum_name"] = forum_name_elm.get_text()

        if forum_desc_elm:
            payload["forum_description"] = forum_desc_elm.get_text()

        threads_count_elm = forums_stats_elm.find("span", class_="forums__stats-count")
        posts_count_elm = forums_stats_sibling_elm.find("span", class_="forums__stats-count")

        payload["forum_threads_count"] = threads_count_elm.get_text() if threads_count_elm else ""
        payload["forum_posts_count"] = posts_count_elm.get_text() if posts_count_elm else ""


        print(payload)