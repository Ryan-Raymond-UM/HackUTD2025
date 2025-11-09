import collections
import duckpy
import ratelimit
import re
import requests
import urllib.parse

def getFirstNonAd(results):
	for result in results:
		url = urllib.parse.urlparse(result['url'])
		if url.netloc != 'duckduckgo.com':
			return result

@ratelimit.sleep_and_retry
@ratelimit.limits(calls=1, period=1)
def guessWebsite(make):
	client = duckpy.Client()
	results = client.search(make)
	return getFirstNonAd(results)['url']

@ratelimit.sleep_and_retry
@ratelimit.limits(calls=1, period=1)
def getProductPage(site, model):
	client = duckpy.Client()
	query = f'site:{site} "{model}"'
	results = client.search(query)
	return getFirstNonAd(results)['url']

def scrape(page):
	response = requests.get(page).text
	pattern = r"\$[1-9]\d{0,2},\d{3}(?:,\d{3})?"
	prices = re.findall(pattern, response)
	print(collections.Counter(prices))

site = guessWebsite('Buick')
print(site)
productPage = getProductPage(site, 'Envista')
print(productPage)
scrape(productPage)
