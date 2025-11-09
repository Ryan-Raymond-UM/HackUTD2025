#!/usr/bin/env python3

import CarAndDriver
import flask
import PIL.Image
import io
import FuelEconomyGov
import math
import IIHS
import openai

CURRENT_YEAR = 2025

app = flask.Flask(__name__)
prompt = """You are a car salesman who is trying to sell the car on the left. Try to convince the customer to buy it using mostly the statistics you have been provided. Use only pure text with no markup or symbols or emojis"""

@app.route('/convince', methods=["POST"])
def convince():
	client = openai.OpenAI(api_key=API_KEY)
	response = client.responses.create(
    model="gpt-4o-mini",
		input=prompt+'\n\n'+flask.request.data.decode()
	)
	return response.output_text

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

@app.route('/photos/<vehicleID>')
def get_photo(vehicleID):
	binary = FuelEconomyGov.getLabel(vehicleID)
	img = PIL.Image.open(io.BytesIO(binary))
	buffer = io.BytesIO()
	img.crop((70, 170, 290, 280)).save(buffer, format='PNG')
	response = flask.make_response(buffer.getvalue())
	response.headers['Content-Type'] = 'image/png'
	return response

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
