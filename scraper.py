import time
from bs4 import BeautifulSoup
import requests


class Scraper():

    headers = {
        'User-Agent': 'Scrapper 1.0',
    }

    def __init__(self, logger):
        self._logger = logger

    def page_crawler(self, url: str, max: int):

        pages = {}
        i = 1
        while i <= max:

            page = self.fetch_page(f"{url}{i}")
            soup = BeautifulSoup(page, "lxml")
            pages[i] = soup

            has_next = soup.find(class_="next")

            
            if not has_next:
                break

            i+=1
            time.sleep(2)
        

        pages["nb_pages"] = i
        return pages
            

    def fetch_page(self, url: str, timeout:int =10):
        """Récupère une page avec gestion d'erreurs."""
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=timeout
            )
            response.raise_for_status()
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
