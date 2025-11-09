#!/usr/bin/env python3

import re
import requests

def scout(url):
	url = f'https://archive.org/wayback/available?url={url}'
	response = requests.get(url).json()
	return response['archived_snapshots']['closest']

def scrape(url):
	archive = scout(url)
	response = requests.get(archive['url']).text.replace(',', '')
	range_pattern = r'\$(\d+)[^/]\$(\d+)'
	pattern = r'>\$(\d+)<'
	price = dict()
	range_match = re.search(range_pattern, response)
	if range_match:
		price['low'], price['high'] = map(int, range_match.group())
	else:
		price['low'] = int(re.search(pattern, response).group(1))
	return price

def getPrice(make, model, year=None):
	year_component = f'-{year}' if year else ''
	url = f'https://www.caranddriver.com/{make.lower()}/{model.lower()}{year_component}'
	return scrape(url)

#print(getPrice('Kia', 'Rio', 2018))
