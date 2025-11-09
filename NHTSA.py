#!/usr/bin/env python3

import functools
import io
import pandas
import requests

HOST = 'https://vpic.nhtsa.dot.gov'
API_ROOT = f'{HOST}/api'
SAFETY_ROOT = 'https://api.nhtsa.gov'

@functools.cache
def getAllMakes():
		url = f'{API_ROOT}/vehicles/getallmakes'
		params = {'format': 'csv'}
		data = requests.get(url, params=params).text
		return pandas.read_csv(io.StringIO(data))

@functools.cache
def isMajorMake(make):
		return make in {474, 13281, 467}
		#return len(getModelsForMake(make)) > 10 # Too slow

@functools.cache
def getMajorMakes():
		allMakes = getAllMakes()
		return allMakes[allMakes['make_id'].apply(isMajorMake)]

@functools.cache
def getModelsForMake(make):
	if isinstance(make, int):
		type = 'GetModelsForMakeId'
	else:
		type = 'GetModelsForMake'
	url = f'{API_ROOT}/vehicles/{type}/{make}'
	params = {'format': 'csv'}
	data = requests.get(url, params=params).text
	return pandas.read_csv(io.StringIO(data))

@functools.cache
def getAllModels():
	makes = getMajorMakes()['make_id']
	return pandas.concat([getModelsForMake(make) for make in makes])

@functools.cache
def getVehicleTypesForMakeModel(make, model):
	url = f'{API_ROOT}/vehicles/GetVehicleTypesForMakeModel/{make}/{model}'
	params = {'format': 'json'}
	data = requests.get(url, params=params).json()
	print(data)
	return pandas.read_csv(io.StringIO(data))

@functools.cache
def getVehicleTypesForMake(make):
	if isinstance(make, int):
		type = 'GetVehicleTypesForMakeId'
	else:
		type = 'GetVehicleTypesForMake'
	url = f'{API_ROOT}/vehicles/{type}/{make}'
	params = {'format': 'csv'}
	data = requests.get(url, params=params).text
	return data

@functools.cache
def getModelsForMakeYear(make, year):
	url = f'{API_ROOT}/vehicles/GetModelsForMakeYear/make/{make}/modelyear/{year}'
	params = {'format': 'csv'}
	data = requests.get(url, params=params).text
	return pandas.read_csv(io.StringIO(data))

@functools.cache
def getModelYearsForMake(make):
	years = list(range(2020, 2026))
	return pandas.concat([getModelsForMakeYear(make, year).assign(year=year) for year in years])

@functools.cache
def getYearsForMakeAndModel(make, model):
	modelYears = getModelYearsForMake(make)
	return modelYears[modelYears['model_name'] == model]

@functools.cache
def getVariants(make, model, year):
	url = f'{SAFETY_ROOT}/SafetyRatings/modelyear/{year}/make/{make}/model/{model}'
	print(url)
	response = requests.get(url).json()['Results']
	return pandas.DataFrame(response)
