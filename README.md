## This script is a scraper for the site [quotes.toscrape.com](http://quotes.toscrape.com)

Each available page of quotes is crawled and scrapped.
A data frame containing
- Text 
- Author 
- Tags 
- Author url

will be generated and converted in an excel file 'result.xlsx' in the output directory.

## use it by launching main.py script (python main.py). You can override the number max of scrapped pages in the main method.