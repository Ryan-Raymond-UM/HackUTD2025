#!/usr/bin/env python3

import functools
import pandas
import random
import requests
from xml.etree import ElementTree

SCHEME = 'https'
HOST = 'www.fueleconomy.gov'
BASE_URL = f'{SCHEME}://{HOST}/ws/rest'

def randomCar():
	make = random.choice(getMakes(2025))
	model = random.choice(getModels(make, 2025))
	options = getOptions(make, model, 2025)
	option_key = random.choice(list(options.keys()))
	return {'make': make, 'model': model, 'option': option_key}

@functools.cache
def getModelYears():
	url = f'{BASE_URL}/vehicle/menu/year'
	xml = requests.get(url).text
	root = ElementTree.fromstring(xml)
	years = [int(v.text) for v in root.findall('.//value')]
	return years

@functools.cache
def getMakes(year):
	url = f'{BASE_URL}/vehicle/menu/make'
	params = {'year': year}
	xml = requests.get(url, params=params).text
	root = ElementTree.fromstring(xml)
	makes = [v.text for v in root.findall('.//value')]
	return makes

@functools.cache
def getModels(make, year):
	url = f'{BASE_URL}/vehicle/menu/model'
	params = {'year': year, 'make': make}
	xml = requests.get(url, params=params).text
	root = ElementTree.fromstring(xml)
	models = [v.text for v in root.findall('.//value')]
	return models

@functools.cache
def getOptions(make, model, year):
	url = f'{BASE_URL}/vehicle/menu/options'
	params = {'make': make, 'model': model, 'year': year}
	xml = requests.get(url, params=params).text
	root = ElementTree.fromstring(xml)
	options = {int(i.find("value").text):i.find("text").text for i in root.findall("menuItem")}
	return options

@functools.cache
def getRating(vehicle):
	url = f'{BASE_URL}/vehicle/{vehicle}'
	xml = requests.get(url).text
	root = ElementTree.fromstring(xml)
	record = dict()
	record['highway'] = int(root.findall('city08')[0].text)
	record['city'] = int(root.findall('highway08')[0].text)
	record['combined'] = int(root.findall('comb08')[0].text)
	record['cost'] = int(root.findall('fuelCost08')[0].text)
	record['type'] = root.findall('VClass')[0].text
	return record
