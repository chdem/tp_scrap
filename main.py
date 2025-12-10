
import logging

from logger import setup_logger
from scraper import Scraper

BASE_URL="http://quotes.toscrape.com/page/"

def main():
    logger = setup_logger("crawler", "logs/logs.txt", logging.INFO)

    scraper = Scraper(logger)
    scraper.page_crawler(BASE_URL, 15)

    scraper.save_to_excel("output/report.xlsx")

if __name__=="__main__":
    main()


