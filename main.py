
import logging

from logger import setup_logger
from scraper import Scraper

BASE_URL="http://quotes.toscrape.com/page/"

def main():
    logger = setup_logger("crawler", "logs/logs.txt", logging.INFO)

    scraper = Scraper(logger)
    scraper.page_crawler(BASE_URL, 15)

    scraper.save_to_excel("output/report.xlsx")

    logger.info("Top 5 auteurs :")
    logger.info(scraper.top_5_author())

    logger.info("")
    logger.info("Top 10 tags : ")
    logger.info(scraper.top_X_most_used_tags(10))

    logger.info("")
    logger.info("Longueur moyenne des citations : ")
    logger.info(f"{scraper.mean_quote()} caractères")


if __name__=="__main__":
    main()


