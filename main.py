#!/usr/bin/env python3

import functools
import io
import pandas
import requests

"""

"""

HOST = 'https://vpic.nhtsa.dot.gov'
API_ROOT = f'{HOST}/api'

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

print(getAllMakes())
print(getMajorMakes())
print(getModelsForMake(474))
print(getAllModels())
print(getVehicleTypesForMakeModel('Honda', 'Civic'))
