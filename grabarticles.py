import requests
import time
from bs4 import BeautifulSoup
from pprint import pprint


def scrape_waypoint:
	pages = 179
	current_page = 1;
	article_url_base = 'https://waypoint.vice.com/api/v1/latest?locale=en_us&page={}&per_page=12'

	headers = {
	    'User-Agent': 'waypoint_ebooks 1.0'
	}

	f = open('corpus.txt', 'w+')

	while current_page <= pages:

	    r = requests.get(article_url_base.format(current_page), headers=headers)

	    for article in r.json():
		print(article['data']['title'])

		f.write(article['data']['title'])
		f.write("\n")


		soup = BeautifulSoup(article['data']['body'], 'html5lib')
		article_body = soup.get_text()

		f.write(article_body)
		f.write("\n\n\n")


	    current_page += 1

	    time.sleep(6)

	f.close()


if __name__ == "__main__":
	scrape_waypoint()
