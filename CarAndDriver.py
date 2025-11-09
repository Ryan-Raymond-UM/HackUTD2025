#!/usr/bin/env python3

import re
import requests

def scout(url):
	url = f'https://archive.org/wayback/available?url={url}'
	response = requests.get(url).json()
	archive = response['archived_snapshots']
	print(archive)
	print(url)
	return archive['closest']

def scrape(url):
	archive = f'https://web.archive.org/web/20300000000000/{url}' #scout(url)
	response = requests.get(archive)
	if response.status_code == 404:
		return scrape(url[:url.rfind(' ')])
	response = response.text.replace(',', '')
	range_pattern = r'\$(\d+)[^/]\$(\d+)'
	pattern = r'>\$(\d+)<'
	price = dict()
	range_match = re.search(range_pattern, response)
	if range_match:
		price['low'], price['high'] = int(range_match.group(1)), int(range_match.group(2))
	else:
		price['low'] = int(re.search(pattern, response).group(1))
	return price

def getPrice(make, model, year=None):
	year_component = f'-{year}' if year else ''
	url = f'www.caranddriver.com/{make.lower().replace(' ', '-')}/{model.lower()}{year_component}'
	return scrape(url)

#print(getPrice('Kia', 'Rio', 2018))
