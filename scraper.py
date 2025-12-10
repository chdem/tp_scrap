import time
from bs4 import BeautifulSoup
import pandas as pd
import requests


class Scraper():

    headers = {
        'User-Agent': 'Scrapper 1.0',
    }

    def __init__(self, logger):
        self._logger = logger
        self.__nb_pages_scrapped = 0
        self.__dataframe = None

    @property
    def quotes_df(self):
        return self.__dataframe
    
    @property
    def nb_pages_in_soups(self):
        return self.__nb_pages_scrapped

    def page_crawler(self, url: str, max: int):

        self._logger.info(f"Début du crawl de {url}")
        self._logger.info(f"Max pages : {max}")
        soups = {}
        i = 1
        while i <= max:

            current_url = f"{url}{i}"

            self._logger.info(f"--Scrap de {current_url}")

            page = self.fetch_page(current_url)
            soup = BeautifulSoup(page, "lxml")
            soups[i] = soup

            has_next = soup.find(class_="next")

            
            if not has_next:
                break

            i+=1

            self._logger.info(f"-- Fin du scrap de {current_url}")
            time.sleep(2)

        self.nb_pages_scrapped = i
        self.__dataframe = self.extract_quotes(soups)
        self._logger.info(f"Fin du scrap de {url}")
            

    def fetch_page(self, url: str, timeout:int =10):
        """Récupère une page avec gestion d'erreurs."""
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=timeout
            )
            response.raise_for_status()
            self._logger.info(f"Status : {response.status_code}")
            return response.text

        except requests.Timeout:
            self._logger.error(f"Timeout pour {url}")
            return None

        except ConnectionError:
            self._logger.error(f"Erreur de connexion pour {url}")
            return None

        except requests.exceptions.HTTPError:
            self._logger.error(f"Erreur HTTP {response.status_code}: {url}")
            return None

        except requests.RequestException as e:
            self._logger.error(f"Erreur générale: {e}")
            return None

    def extract_quotes(self, soups)-> pd.DataFrame:
        all_quotes = []
        for page, soup in soups.items():
            quotes = soup.find_all(class_="quote")
            for quote in quotes:
                row = {
                    "quote": quote.find(class_="text").text,
                    "author": quote.find(class_="author").text,
                    "tags": [tag.text for tag in quote.find_all(class_="tag")],
                    "page": page
                    }
                all_quotes.append(row)
        
        return pd.DataFrame(all_quotes)
    
    def extract_tags(self):
        tag_list = {}
        for tags in self.__dataframe["tags"]:
            for tag in tags:
                tag_list[tag] = tag_list.get(tag, 0) + 1

        return pd.DataFrame(
            list(tag_list.items()),
            columns=['tag', 'count']
            )

    def get_author_df(self):
        return (
            self.__dataframe
                .groupby("author", as_index=False)
                .agg(count=("quote", "count"))
                )
    
    def save_to_excel(self, file):
        with pd.ExcelWriter(file, mode="w", engine="openpyxl") as writer:
            self.__dataframe.to_excel(writer, sheet_name="données", index=False)
            self.get_author_df().to_excel(writer, sheet_name="authors", index=False)
            self.extract_tags().to_excel(writer, sheet_name="tags", index=False)

    def top_5_author(self):
        df = self.__dataframe
        return df['author'].value_counts().head(5)
    
    def top_X_most_used_tags(self, top: int):
        return self.extract_tags().sort_values("count", ascending=False).head(top).reset_index()

    def mean_quote(self):
        return self.__dataframe["quote"].str.len().mean()