#!/usr/bin/env python3

import CarAndDriver
import flask
import FuelEconomyGov
import math
import IIHS

CURRENT_YEAR = 2025
API_KEY = 'AIzaSyBLMH4gA6a1f62uOBoEc2_3ZTCwvTHB6Jk'

app = flask.Flask(__name__)

@app.route('/makes')
def get_makes():
	return FuelEconomyGov.getMakes(CURRENT_YEAR)

@app.route('/makes/<make>/models')
def get_models(make):
	return FuelEconomyGov.getModels(make, CURRENT_YEAR)

@app.route('/makes/<make>/models/<model>/options')
def get_options(make, model, year=2025):
	return FuelEconomyGov.getOptions(make, model, year)

@app.route('/makes/<make>/models/<model>/pricing')
def get_pricing(make, model):
	pricing = CarAndDriver.getPrice(make, model)
	return pricing

@app.route('/makes/<make>/models/<model>/deaths')
def get_deaths(make, model):
	deaths = IIHS.get_deaths((make, model.split(' ', 1)[0]))
	deaths = deaths['OverallDeathRate'].dropna().mean()
	print('DEATHS', deaths)
	return {'deaths': (deaths if (deaths and not math.isnan(deaths)) else 'not enough data')}

@app.route('/fuel/<vehicleID>')
def get_fuel(vehicleID):
	return FuelEconomyGov.getRating(vehicleID)

@app.route('/makes/<make>/models/<model>/insurance')
def get_insurance(make, model):
	deaths = IIHS.get_insurance_rates((make, model.split(' ', 1)[0]))
	deaths = deaths['AllCoverages'].dropna().mean()
	print('INSURANCE', deaths)
	return {'insurance': (deaths if (deaths and not math.isnan(deaths)) else 'not enough data')}

@app.route('/types/<type>')
def get_from_type(type):
	# Figure out cars to compare against
	return FuelEconomyGov.randomCar()

app.run()
