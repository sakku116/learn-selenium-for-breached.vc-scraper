import cfscrape
from bs4 import BeautifulSoup

# get page using cloudflare scraper to bypass ddos protection
scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
home_page = scraper.get("https://breached.to")

soup = BeautifulSoup(home_page.content.decode("utf-8") , "html.parser")

print(soup.find("a", class_="forums__forum-name"))