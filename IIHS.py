#!/usr/bin/env python3

import functools
import json
import multiprocessing.dummy
import pandas
import requests

url = 'https://www.iihs.org/api/driver-death-rates/get-view-model'

@functools.cache
def get_parameters():
	response = requests.post(url).json()
	sizes = {s['Id'] for s in response['Sizes']}
	styles = {s['Id'] for s in response['Styles']}
	return sizes, styles

@functools.cache
def get_page(size, style):
	params = {
		"query": {
			"VehicleStyleId": style,
			"VehicleSizeId": size}
		}
	response = requests.post(url, json=params)
	return response.json()['Info']

def get_deaths(make_and_model=None):
	deaths = pandas.read_csv('deaths.csv', index_col=0)
	if make_and_model:
		return deaths.loc[deaths.index.str.lower().str.startswith(' '.join(make_and_model).lower())]
	else:
		return deaths
	sizes, styles = get_parameters()

	all_records = []
	for size in sizes:
		for style in styles:
				all_records += get_page(size, style)

	deaths = pandas.DataFrame(all_records)
	if make_and_model:
	  deaths = deaths[deaths['Vehicle'].map(lambda name: name.lower().startswith(' '.join(make_and_model).lower()))]
	return deaths

def get_insurance_rates(make_and_model):
	deaths = pandas.read_csv('insurance_rates.csv', index_col=0)
	if make_and_model:
		return deaths.loc[deaths.index.str.lower().str.startswith(' '.join(make_and_model).lower())]
	else:
		return deaths

	p = multiprocessing.dummy.Pool()
	styles = list(range(1,15))
	sizes = list(range(6))
	url = 'https://www.iihs.org/api/hldilosses/getviewmodel'
	slices = list()
	for style in styles:
		for size in sizes:
			json = {"query":{"ModelYears":"2020-2022","VehicleClassId":style,"VehicleSizeId":size,"Coverage":"collision","SortColumn":"Vehicle"}}
			slices = slices + requests.post(url, json=json).json()['VehiclesByClass']
	df = pandas.DataFrame(slices).set_index('Vehicle', drop=True)
	df = df.map(lambda x: x['Percentage'])
	return df

#get_deaths().to_csv('deaths.csv')
