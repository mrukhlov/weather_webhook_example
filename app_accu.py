import os
from wwo_api import wwo_weather_get
from accu_api import (
	accu_weather_get_daily,
	accu_weather_get_current,
	accu_weather_get_hourly,
)
from country_codes import codes
import requests
from datetime import datetime, timedelta

from flask import (
	Flask,
	request,
	make_response,
	jsonify
)

app = Flask(__name__)
log = app.logger

apikey = '7UmuyhWz6qteGNoQRusNzXA9M0Ccwlf8'

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

	parameters = req['result']['parameters']
	address = parameters.get('address')
	date_time = parameters.get('date-time')
	unit = parameters.get('unit')

	if date_time:
		date = date_time.get('date')
		time = date_time.get('time')

	if address:
		city = address.get('city')
		country = address.get('country')
		if country == 'Russian Federation': country = 'Russia'
		if not city:
			send_url = 'http://ipinfo.io'
			r = requests.get(send_url)
			if codes[r.json().get('country')] == country:
				city = r.json().get('city')
	else:
		send_url = 'http://ipinfo.io'
		r = requests.get(send_url)
		city = r.json().get('city')
		country = codes[r.json().get('country')]

	if city:
		# wwo = wwo_weather_get(parameters['address']['city'])
		# if wwo:
		# 	city = wwo['request'][0]['query']
		# 	temp = wwo['current_condition'][0]['temp_C']
		#
		# 	wwo_resp = 'Weather in %s is %s degrees celsius' % (city, temp)
		# 	print wwo_resp

		if date_time:
			if date:
				accu = accu_weather_get_daily(city, apikey, country, unit)
			if time and not date:
				accu = accu_weather_get_hourly(city, apikey, country, unit)
		else:
			accu = accu_weather_get_current(city, apikey, country)

		if accu:
			if date_time:
				date_dict = {}
				time_dict = {}
				if date:
					for day in accu['DailyForecasts']:
						if day['Date'].find(date) > -1:
							date_dict = day['Temperature']
				if time and not date:
					for hour in accu:
						if datetime.strptime(hour['DateTime'][:-6], '%Y-%m-%dT%H:%M:%S').hour == datetime.strptime(time, '%H:%M:%S').hour:
							time_dict = hour

				accu_resp = 'Date is too far.'

				if date_dict:
					temp = (date_dict['Minimum']['Value'] + date_dict['Maximum']['Value']) / 2
					if unit and unit == 'C':
						unit = 'celsius'
					else:
						unit = 'fahrenheit'
					accu_resp = 'Weather in %s on %s will be %s degrees %s. ' \
					            'Minimum is %s degrees and maximum is %s' % (
						city,
						date,
						int(temp),
						unit,
						int(date_dict['Minimum']['Value']),
						int(date_dict['Maximum']['Value'])
					)
				if time_dict:
					temp = time_dict['Temperature']['Value']
					if unit and unit == 'C':
						unit = 'celsius'
					else:
						unit = 'fahrenheit'
					accu_resp = 'Weather in %s on %s will be %s degrees %s.' % (city, time, int(temp), unit)
			else:
				text = accu[0]['WeatherText']
				if unit and unit == 'C':
					temp = accu[0]["Temperature"]["Metric"]["Value"]
					unit = 'celsius'
				else:
					temp = accu[0]["Temperature"]["Imperial"]["Value"]
					unit = 'fahrenheit'
				accu_resp = 'Weather in %s is %s degrees %s, %s' % (city, temp, unit, text)

		else:
			accu_resp = 'Couldn\'t find'

		return accu_resp
	else:
		return 'Please specify city.'

def weather_activity(req):
	pass

def weather_condition(req):
	pass

def weather_outfit(req):
	pass

def weather_temperature(req):
	pass

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