import os
from wwo_api import wwo_weather_get

from weather_response import (
	weather_response_current,
	weather_response_date,
	weather_response_time_period,
	weather_response_date_period
)

from weather_data_process import (
	weather_current,
	weather_date,
	weather_time,
	weather_date_period,
	weather_time_period,
	adress_getter
)

from flask import (
	Flask,
	request,
	make_response,
	jsonify
)

app = Flask(__name__)
log = app.logger

apikey = '7UmuyhWz6qteGNoQRusNzXA9M0Ccwlf8'

unit_global = ''

@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)
	try:
		action = req.get("result").get('action')
	except AttributeError:
		return 'json error'

	if action == 'weather':
		res = weather(req)
	elif action == 'weather.activity':
		res = weather_activity(req)
	elif action == 'weather.condition':
		res = weather_condition(req)
	elif action == 'weather.outfit':
		res = weather_outfit(req)
	elif action == 'weather.temperature':
		res = weather_temperature(req)
	else:
		log.error("Unexpeted action.")

	return make_response(jsonify(res))

def weather(req):

	parameters = adress_getter(req['result']['parameters'])
	address = parameters.get('address')
	date_time = parameters.get('date-time')
	city = address.get('city')
	unit = parameters.get('unit')
	if not unit:
		if len(unit_global) > 0:
			parameters['unit'] = unit_global

	if city:

		wwo = wwo_weather_get(parameters)
		error = wwo.get('error')

		if not error:
			'''if we get date and time parameters'''
			if date_time:

				date = date_time.get('date')
				time = date_time.get('time')
				date_period = date_time.get('date-period')
				time_period = date_time.get('time-period')

				if time:
					city, date, time, temp, unit, weather_data = weather_time(parameters, wwo)
					resp = 'Weather in %s on %s %s will be %s degrees %s.' % (city, date, time, temp, unit)
				if date and not time:
					city, date, temp, unit, min_temp, max_temp, weather_data = weather_date(parameters, wwo)
					resp = weather_response_date(city, date, temp, unit, min_temp, max_temp)
				elif date_period:
					city, date_start, date_end, degree_list, condition_list, weather_data = weather_date_period(parameters, wwo)
					resp = weather_response_date_period(city, date_start, date_end, degree_list, condition_list)
				elif time_period:
					city, time_start, time_end, degree_list, condition_list, weather_data = weather_time_period(parameters, wwo)
					resp = weather_response_time_period(city, time_start, time_end, degree_list, condition_list)
			else:
				'''else we just return current conditions'''
				city, temp, desc, unit, weather_data = weather_current(parameters, wwo)
				resp = weather_response_current(city, temp, desc, unit)
		else:
			resp = error

		return {"speech": resp, "displayText": resp}
	else:
		return 'Please specify city.'

def weather_activity(req):

	winter_activity = ['skiing', 'snowboarding']
	summer_activity = ['cycling', 'run', 'swimming', 'jogging', 'hiking', 'skating', 'parasailing', 'widsurfing']
	demi_activity = []

	parameters = adress_getter(req['result']['parameters'])
	address = parameters.get('address')
	city = address.get('city')
	date_time = parameters.get('date-time')
	activity = parameters.get('activity')
	unit = parameters.get('unit')
	if not unit:
		if len(unit_global) > 0:
			parameters['unit'] = unit_global

	if city:

		wwo = wwo_weather_get(parameters)
		error = wwo.get('error')

		if not error:
			'''if we get date and time parameters'''
			if date_time:

				date = date_time.get('date')
				time = date_time.get('time')
				date_period = date_time.get('date-period')
				time_period = date_time.get('time-period')

				if time:
					city, date, time, temp, unit, weather_data = weather_time(parameters, wwo)
					if activity in winter_activity:
						if temp < 0:
							resp = 'Weather in %s on %s %s will be %s degrees %s. Perfect conditions for %s!' % (city, date, time, temp, unit, activity)
						else:
							resp = 'Weather in %s on %s %s will be %s degrees %s. Not a best weather for %s.' % (city, date, time, temp, unit, activity)
					elif activity in summer_activity:
						if temp > 0:
							resp = 'Weather in %s on %s %s will be %s degrees %s. Perfect conditions for %s!' % (city, date, time, temp, unit, activity)
						else:
							resp = 'Weather in %s on %s %s will be %s degrees %s. Not a best weather for %s.' % (city, date, time, temp, unit, activity)
				if date and not time:
					city, date, temp, unit, min_temp, max_temp, weather_data = weather_date(parameters, wwo)
					if activity in winter_activity:
						if temp < 0:
							resp = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s. Perfect weather for %s!' % (city, date, temp, unit, min_temp, max_temp, activity)
						else:
							resp = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s. Not a best weathe for %s.' % (city, date, temp, unit, min_temp, max_temp, activity)
					elif activity in summer_activity:
						if temp > 0:
							resp = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s. Perfect weather for %s!' % (city, date, temp, unit, min_temp, max_temp, activity)
						else:
							resp = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s. Not a best weathe for %s.' % (city, date, temp, unit, min_temp, max_temp, activity)
				elif date_period:
					city, date_start, date_end, degree_list, weather_data = weather_date_period(parameters, wwo)
					resp = 'The weather in %s on period from %s till %s will be: %s. What a weather for %s.' % (city, date_start, date_end, str(degree_list), activity)
				elif time_period:
					city, date_start, date_end, degree_list, weather_data = weather_time_period(parameters, wwo)
					resp = 'The weather in %s on period from %s till %s will be: %s. What a weather for %s.' % (city, date_start, date_end, str(degree_list), activity)
			else:
				'''else we just return current conditions'''
				city, temp, desc, unit, weather_data = weather_current(parameters, wwo)
				if activity in winter_activity:
					if temp < 0:
						resp = 'Weather in %s is %s degrees %s. %s. What a perfect weather for %s!' % (city, temp, unit, desc, activity)
					else:
						resp = 'Weather in %s is %s degrees %s. %s. Not a best weather for %s.' % (city, temp, unit, desc, activity)
				elif activity in summer_activity:
					if temp > 0:
						resp = 'Weather in %s is %s degrees %s. %s. What a perfect weather for %s!' % (city, temp, unit, desc, activity)
					else:
						resp = 'Weather in %s is %s degrees %s. %s. Not a best weather for %s.' % (city, temp, unit, desc, activity)
				else:
					resp = 'What sport is this?'
		else:
			resp = error

		return {"speech": resp, "displayText": resp}
	else:
		return 'Please specify location.'

def weather_condition(req):
	supported = ['rain', 'snow', 'wind', 'sun', 'fog', 'thunder', 'overcast', 'clouds', 'foggy']
	unsupported = ['shower', 'ice', 'freezing rain', 'rain snow', 'haze', 'smoke']

	parameters = adress_getter(req['result']['parameters'])
	address = parameters.get('address')
	date_time = parameters.get('date-time')
	city = address.get('city')
	condition = parameters.get('condition')
	unit = parameters.get('unit')
	if not unit:
		if len(unit_global) > 0:
			parameters['unit'] = unit_global

	if condition in unsupported:
		error = 'Unsupported condition'
		return error
	else:
		parameters['condition_original'] = condition
		if condition == 'rain':
			parameters['condition'] = "chanceofrain"
		elif condition == 'snow':
			parameters['condition'] = "chanceofsnow"
		elif condition == 'wind':
			parameters['condition'] = "chanceofwindy"
		elif condition == 'sun':
			parameters['condition'] = "chanceofsunshine"
		elif condition == 'fog' or condition == 'foggy':
			parameters['condition'] = "chanceoffog"
		elif condition == 'thunder':
			parameters['condition'] = "chanceofthunder"
		elif condition == 'overcast':
			parameters['condition'] = "chanceofovercast"
		elif condition == 'clouds':
			parameters['condition'] = "cloudcover"
		condition_original = parameters['condition_original']
	if city:

		wwo = wwo_weather_get(parameters)
		error = wwo.get('error')

		if not error:
			'''if we get date and time parameters'''
			if date_time:

				date = date_time.get('date')
				time = date_time.get('time')
				date_period = date_time.get('date-period')
				time_period = date_time.get('time-period')

				if time:
					city, date, time, temp, unit, condition, weather_data = weather_time(parameters, wwo)
					resp = 'Weather in %s on %s %s will be %s degrees %s. Chance of %s is %s percent.' % (city, date, time, temp, unit, condition_original, condition)
				if date and not time:
					city, date, temp, unit, min_temp, max_temp, condition, weather_data = weather_date(parameters, wwo)
					resp = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s. Chance of %s is %s percent.' % (city, date, temp, unit, min_temp, max_temp, condition_original, condition)
				elif date_period:
					city, date_start, date_end, degree_list, condition_list, weather_data = weather_date_period(parameters, wwo)
					resp = 'The weather in %s on period from %s till %s will be: %s. Chance of %s is %s percent.' % (city, date_start, date_end, str(degree_list), condition_original, str(condition_list))
				elif time_period:
					city, date_start, date_end, degree_list, condition_list, weather_data = weather_time_period(parameters, wwo)
					resp = 'The weather in %s on period from %s till %s will be: %s. Chance of %s is %s percent.' % (city, date_start, date_end, str(degree_list), condition_original, str(condition_list))
			else:
				'''else we just return current conditions'''
				city, temp, desc, condition, unit, weather_data = weather_current(parameters, wwo)
				resp = 'Weather in %s is %s degrees %s. %s. Chance of %s is %s percent.' % (city, temp, unit, desc, condition_original, condition)
		else:
			resp = error

		return {"speech": resp, "displayText": resp}
	else:
		return 'Please specify location.'

def weather_outfit(req):

	cold_weather = ['wool socks', 'wool cap', 'turtleneck', 'thermal pants', 'sweatshirt', 'sweatpants', 'sweater', 'snowboard pants', 'ski pants', 'shawls', 'scarf','jumper','balaclava', 'beanie', 'boots', 'cardigan', 'fleece top', 'gloves']
	warm_weather = ['umbrella', 'tennis shoes', 'lounge wear', 'socks', 'sneakers', 'sleeve shirt', 'rain pants','rain jacket','rain coat','pants','khakis','jeans', 'jacket', 'casual shirt', 'coat', 'dress pants', 'dress shirt', 'dress', 'gum boots', 'hat', 'hoodie']
	hot_weather = ['tank top', 't-shirt', 'swimwear', 'swim goggles', 'sunscreen', 'sunglasses', 'skirt', 'shorts', 'bathing suit', 'bra', 'capri', 'flips flops', 'pool shoes', 'sandals']
	unknown = ['underwear', 'tie', 'neck gaiter', 'pajama', 'sleepwear', 'slippers', 'suit']

	rain = ['umbrella', 'coat', 'gum boots', 'beanie', 'hat', 'jacket', 'rain coat', 'rain jacket', 'rain pants']
	snow = ['gloves', 'fleece top', 'ski pants', 'snowboard pants']
	sun = ['swimwear', 'swim goggles', 'bra', 'bathing suit', 'flips flops', 'sandals', 'sunglasses', 'sunscreen']

	parameters = adress_getter(req['result']['parameters'])
	address = parameters.get('address')
	date_time = parameters.get('date-time')
	city = address.get('city')
	outfit = parameters.get('outfit')

	unit = parameters.get('unit')
	if not unit:
		if len(unit_global) > 0:
			parameters['unit'] = unit_global

	if outfit:
		if outfit in cold_weather or outfit in warm_weather or outfit in hot_weather:
			if outfit in cold_weather:
				temp_limit = -5
			if outfit in warm_weather:
				temp_limit = 10
			if outfit in hot_weather:
				temp_limit = 20
		if outfit in rain or outfit in snow or outfit in sun:
			if outfit in rain:
				parameters['condition'] = 'chanceofrain'
				parameters['condition_original'] = 'rain'
			elif outfit in snow:
				parameters['condition'] = 'chanceofsnow'
				parameters['condition_original'] = 'snow'
			else:
				parameters['condition'] = 'chanceofsunshine'
				parameters['condition_original'] = 'sun'
			condition_original = parameters['condition_original']

	if city:

		wwo = wwo_weather_get(parameters)
		error = wwo.get('error')

		if not error:
			'''if we get date and time parameters'''
			if date_time:

				date = date_time.get('date')
				time = date_time.get('time')
				date_period = date_time.get('date-period')
				time_period = date_time.get('time-period')

				if time:
					if outfit in rain or outfit in snow or outfit in sun:
						city, date, time, temp, unit, condition, weather_data = weather_time(parameters, wwo)
						if outfit in cold_weather or outfit in warm_weather or outfit in hot_weather:
							# to change maybe
							if condition > 50:
								resp = 'Weather in %s on %s %s will be %s degrees %s. Chance of %s is %s percent. You probably need %s.' % (city, date, time, temp, unit, condition_original, condition, outfit)
							else:
								resp = 'Weather in %s on %s %s will be %s degrees %s. Chance of %s is %s percent. You probably don\'t need %s.' % (city, date, time, temp, unit, condition_original, condition, outfit)
						else:
							if condition > 50:
								resp = 'Weather in %s on %s %s will be %s degrees %s. Chance of %s is %s percent. You probably need %s.' % (city, date, time, temp, unit, condition_original, condition, outfit)
							else:
								resp = 'Weather in %s on %s %s will be %s degrees %s. Chance of %s is %s percent. You probably don\'t need %s.' % (city, date, time, temp, unit, condition_original, condition, outfit)
					else:
						city, date, time, temp, unit, weather_data = weather_time(parameters, wwo)
						if temp_limit > 0:
							if temp > temp_limit:
								resp = 'Weather in %s on %s %s will be %s degrees %s. Probably it\'s too hot for %s.' % (city, date, time, temp, unit, outfit)
							else:
								resp = 'Weather in %s on %s %s will be %s degrees %s. Weather is perfect for %s!' % (city, date, time, temp, unit, outfit)
						else:
							if temp > temp_limit:
								resp = 'Weather in %s on %s %s will be %s degrees %s. You probably don\'t need %s.' % (city, date, time, temp, unit, outfit)
							else:
								resp = 'Weather in %s on %s %s will be %s degrees %s. Weather is cold, please wear %s!' % (city, date, time, temp, unit, outfit)
				if date and not time:
					if outfit in rain or outfit in snow or outfit in sun:
						city, date, temp, unit, min_temp, max_temp, condition, weather_data = weather_date(parameters, wwo)
						if condition > 50:
							resp = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s. Chance of %s is %s percent. You probably need %s.' % (city, date, temp, unit, min_temp, max_temp, condition_original, condition, outfit)
						else:
							resp = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s. Chance of %s is %s percent. You probably don\'t need %s.' % (city, date, temp, unit, min_temp, max_temp, condition_original, condition, outfit)
					else:
						city, date, temp, unit, min_temp, max_temp, weather_data = weather_date(parameters, wwo)
						if temp_limit > 0:
							if temp > temp_limit:
								resp = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s. Probably it\'s too hot for %s.' % (city, date, temp, unit, min_temp, max_temp, outfit)
							else:
								resp = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s. Weather is perfect for %s!' % (city, date, temp, unit, min_temp, max_temp, outfit)
						else:
							if temp > temp_limit:
								resp = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s. You probably don\'t need %s.' % (city, date, temp, unit, min_temp, max_temp, outfit)
							else:
								resp = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s. Weather is cold, please wear %s!' % (city, date, temp, unit, min_temp, max_temp, outfit)
				elif date_period:
					city, date_start, date_end, degree_list, weather_data = weather_date_period(parameters, wwo)
					resp = 'The weather in %s on period from %s till %s will be: %s' % (city, date_start, date_end, str(degree_list))
				elif time_period:
					city, date_start, date_end, degree_list, weather_data = weather_time_period(parameters, wwo)
					resp = 'The weather in %s on period from %s till %s will be: %s.' % (city, date_start, date_end, str(degree_list))
			else:
				'''else we just return current conditions'''
				city, temp, desc, condition, unit, weather_data = weather_current(parameters, wwo)
				if outfit in rain or outfit in snow or outfit in sun:
					if condition > 50:
						resp = 'Weather in %s is %s degrees %s. %s. Chance of %s is %s percent. You probably need %s.' % (city, temp, unit, desc, condition_original, condition, outfit)
					else:
						resp = 'Weather in %s is %s degrees %s. %s. Chance of %s is %s percent. You probably don\'t need %s.' % (city, temp, unit, desc, condition_original, condition, outfit)
				else:
					if temp_limit > 0:
						if temp > temp_limit:
							resp = 'Weather in %s is %s degrees %s. %s. Probably it\'s too hot for %s.' % (city, temp, unit, desc, outfit)
						else:
							resp = 'Weather in %s is %s degrees %s. %s. Weather is perfect for %s!' % (city, temp, unit, desc, outfit)
					else:
						if temp > temp_limit:
							resp = 'Weather in %s is %s degrees %s. %s. You probably don\'t need %s.' % (city, temp, unit, desc, outfit)
						else:
							resp = 'Weather in %s is %s degrees %s. %s. Weather is cold, please wear %s!' % (city, temp, unit, desc, outfit)
		else:
			resp = error

		return {"speech": resp, "displayText": resp}
	else:
		return 'Please specify city.'

def weather_temperature(req):

	parameters = adress_getter(req['result']['parameters'])
	address = parameters.get('address')
	date_time = parameters.get('date-time')
	unit = parameters.get('unit')
	city = address.get('city')
	temperature = parameters['temperature']

	unit = parameters.get('unit')
	if not unit:
		if len(unit_global) > 0:
			parameters['unit'] = unit_global

	if temperature:
		if temperature == 'hot':
			temp_limit = 20
		if temperature == 'warm':
			temp_limit = 15
		if temperature == 'chilly':
			temp_limit = 5
		if temperature == 'cold':
			temp_limit = -5

	if city:

		wwo = wwo_weather_get(parameters)
		error = wwo.get('error')

		if not error:
			'''if we get date and time parameters'''
			if date_time:

				date = date_time.get('date')
				time = date_time.get('time')
				date_period = date_time.get('date-period')
				time_period = date_time.get('time-period')

				if time:
					city, date, time, temp, unit, weather_data = weather_time(parameters, wwo)
					if not temperature:
						resp = 'Weather in %s on %s %s will be %s degrees %s.' % (city, date, time, temp, unit)
					else:
						if temp_limit > 0:
							if temp < temp_limit:
								resp = 'Weather in %s on %s %s will be %s degrees %s. It\'s not too %s outside.' % (city, date, time, temp, unit)
							else:
								resp = 'Weather in %s on %s %s will be %s degrees %s.' % (city, date, time, temp, unit)
						else:
							if temp > temp_limit:
								resp = 'Weather in %s on %s %s will be %s degrees %s. It\'s not too %s outside.' % (city, date, time, temp, unit)
							else:
								resp = 'Weather in %s on %s %s will be %s degrees %s.' % (city, date, time, temp, unit)
				if date and not time:
					city, date, temp, unit, min_temp, max_temp, weather_data = weather_date(parameters, wwo)
					if not temperature:
						resp = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s.' % (city, date, temp, unit, min_temp, max_temp)
					else:
						if temp_limit > 0:
							if temp < temp_limit:
								resp = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s. It\'s not too %s outside.' % (city, date, temp, unit, min_temp, max_temp, temperature)
							else:
								resp = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s. It\'s definitely %s outside.' % (city, date, temp, unit, min_temp, max_temp, temperature)
						else:
							if temp > temp_limit:
								resp = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s. It\'s not too %s outside.' % (city, date, temp, unit, min_temp, max_temp, temperature)
							else:
								resp = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s. It\'s definitely %s outside.' % (city, date, temp, unit, min_temp, max_temp, temperature)
				elif date_period:
					city, date_start, date_end, degree_list, weather_data = weather_date_period(parameters, wwo)
					resp = 'The weather in %s on period from %s till %s will be: %s' % (city, date_start, date_end, str(degree_list))
				elif time_period:
					city, date_start, date_end, degree_list, weather_data = weather_time_period(parameters, wwo)
					resp = 'The weather in %s on period from %s till %s will be: %s.' % (city, date_start, date_end, str(degree_list))
			elif unit:
				global unit_global
				unit_global = unit
				resp = 'Okay, i will show weather in %s.' % (unit_global)
			else:
				'''else we just return current conditions'''
				city, temp, desc, unit, weather_data = weather_current(parameters, wwo)
				if not temperature:
					resp = 'Weather in %s is %s degrees %s. %s.' % (city, temp, unit, desc)
				else:
					if temp_limit > 0:
						if temp < temp_limit:
							resp = 'Weather in %s is %s degrees %s. %s. It\'s not too %s outside.' % (city, temp, unit, desc, temperature)
						else:
							resp = 'Weather in %s is %s degrees %s. %s. It\'s definitely %s outside.' % (city, temp, unit, desc, temperature)
					else:
						if temp > temp_limit:
							resp = 'Weather in %s is %s degrees %s. %s. It\'s not too %s outside.' % (city, temp, unit, desc, temperature)
						else:
							resp = 'Weather in %s is %s degrees %s. %s. It\'s definitely %s outside.' % (city, temp, unit, desc, temperature)
		else:
			resp = error
		print unit_global
		return {"speech": resp, "displayText": resp}
	else:
		return 'Please specify city.'

@app.route('/test', methods=['GET'])
def test():
	return 'weather agent'

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

	app.run(
		debug=True,
		port=port,
		host='0.0.0.0'
	)