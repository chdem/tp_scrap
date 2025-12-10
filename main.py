
import logging

from logger import setup_logger
from scraper import Scraper


BASE_URL="http://quotes.toscrape.com/page/"

def main():
    logger = setup_logger("crawler", "logs/logs.txt", logging.INFO)

    scraper = Scraper(logger)
    pages = scraper.page_crawler(BASE_URL, 15)

    print(pages)

if __name__=="__main__":
    main()
