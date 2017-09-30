import requests
import time
import math
from bs4 import BeautifulSoup
from pprint import pprint

def scrape_waypoint():
    current_page = 1
    articles_per_page = 12
    corpusFile = './data/corpus.txt'

    article_url_base = 'https://waypoint.vice.com/api/v1/latest?locale=en_us&page={}&per_page={}'

    headers = {
        'User-Agent': 'waypoint_ebooks 1.0'
    }
    #determine total number of pages from api headers
    total_request = requests.get(article_url_base.format(current_page,articles_per_page), headers=headers)
    total_articles = int(total_request.headers['x-total-count'])
    total_pages = math.ceil(total_articles/articles_per_page)

    f = open(corpusFile, 'w+')

    while current_page <= total_pages:

        r = requests.get(article_url_base.format(current_page,articles_per_page), headers=headers)

        for article in r.json():
            print(article['data']['title'])

            f.write(article['data']['title'])
            f.write("\n")

            soup = BeautifulSoup(article['data']['body'], 'html5lib')
            article_body = soup.get_text()

            f.write(article_body)
            f.write("\n\n\n")

        current_page += 1

        time.sleep(5)

    f.close()

if __name__ == "__main__":
    scrape_waypoint()
