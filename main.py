
import logging

from logger import setup_logger
from scraper import Scraper

BASE_URL="http://quotes.toscrape.com/page/"

def main():
    logger = setup_logger("crawler", "logs/logs.txt", logging.INFO)

    scraper = Scraper(logger)
    scraper.page_crawler(BASE_URL, 15)

    scraper.save_to_excel("output/report.xlsx")

    print("Top 5 auteurs :")
    print(scraper.top_5_author())

    print()
    print("Top 10 tags : ")
    print(scraper.top_X_most_used_tags(10))

    print()
    print("Longueur moyenne des citations : ")
    print(f"{scraper.mean_quote()} caractères")


if __name__=="__main__":
    main()


