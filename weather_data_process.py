from datetime import datetime
import time as py_time
from country_codes import codes
import requests

def adress_getter(parameters):

	address = parameters.get('address')

	if address:
		city = address.get('city')
		country = address.get('country')
		if country and country == 'Russian Federation': country = 'Russia'
		if not city:
			send_url = 'http://ipinfo.io'
			r = requests.get(send_url)
			if codes[r.json().get('country')] == country:
				city = r.json().get('city')
				if city:
					parameters['address']['city'] = city
	else:
		parameters['address'] = {}
		send_url = 'http://ipinfo.io'
		r = requests.get(send_url)
		city = r.json().get('city')
		country = codes[r.json().get('country')]
		if city:
			parameters['address']['city'] = city
		if country:
			parameters['address']['country'] = country
			parameters['address']['country_code'] = r.json().get('country')

	return parameters

def weather_date(parameters, wwo):

	address = parameters.get('address')
	unit = parameters.get('unit')
	condition = parameters.get('condition')
	city = address.get('city')

	weather = wwo['weather'][0]
	date = weather['date']
	if unit and unit == 'C':
		max_temp = int(weather['maxtempC'])
		min_temp = int(weather['mintempC'])
		unit = 'celsius'
	elif unit and unit == 'F':
		max_temp = int(weather['maxtempF'])
		min_temp = int(weather['mintempF'])
		unit = 'fahrenheit'
	else:
		max_temp = int(weather['maxtempC'])
		min_temp = int(weather['mintempC'])
		unit = 'celsius'

	temp = (max_temp + min_temp) / 2

	if not condition:
		return city, date, int(temp), unit, min_temp, max_temp
	else:
		time = wwo['current_condition'][0]["observation_time"]
		time = py_time.strptime(time, '%I:%M %p')
		if time.tm_hour != 0:
			time = str(time.tm_hour) + '00'
		else:
			time = str(time.tm_hour)
		for hour in wwo["weather"][0]['hourly']:
			if hour['time'] == time:
				condition = hour[condition]

		return city, date, int(temp), unit, min_temp, max_temp, int(condition)

def weather_time(parameters, wwo):

	address = parameters.get('address')
	date_time = parameters.get('date-time')
	unit = parameters.get('unit')
	condition = parameters.get('condition')

	city = address.get('city')
	time = date_time.get('time')
	weather = wwo['weather'][0]
	date = weather['date']

	if datetime.strptime(time, '%H:%M:%S').hour == 0:
		params_hour = str(datetime.strptime(time, '%H:%M:%S').hour)
	else:
		params_hour = str(datetime.strptime(time, '%H:%M:%S').hour) + '00'

	for hour_data in weather['hourly']:
		if params_hour == hour_data['time']:
			if condition:
				condition = hour_data[condition]
			if unit and unit == 'C':
				temp = hour_data['tempC']
				unit = 'celsius'
			elif unit and unit == 'F':
				temp = hour_data['tempF']
				unit = 'fahrenheit'
			else:
				temp = hour_data['tempC']
				unit = 'celsius'

	if not condition:
		return city, date, time, int(temp), unit
	else:
		return city, date, time, int(temp), unit, int(condition)

def weather_date_period(parameters, wwo):

	address = parameters.get('address')
	date_time = parameters.get('date-time')
	unit = parameters.get('unit')
	condition = parameters.get('condition')

	date_period = date_time.get('date-period')
	city = address.get('city')

	degree_list = []
	condition_list = []
	dates = date_period.split('/')
	weather = wwo['weather']
	for date in weather:
		if datetime.strptime(date['date'], '%Y-%m-%d') >= datetime.strptime(dates[0], '%Y-%m-%d') or datetime.strptime(date['date'], '%Y-%m-%d') <= datetime.strptime(dates[1], '%Y-%m-%d'):
			# if condition:
			for hour in date['hourly']:
				if hour['time'] == '1200':
					if condition:
						condition_list.append(hour[condition])
					else:
						condition_list.append(hour['weatherDesc'][0]["value"].lower())
			if unit and unit == 'C':
				degree_list.append([(int(date['maxtempC']) + int(date['mintempC'])) / 2, int(date['maxtempC']), int(date['mintempC'])])
			elif unit and unit == 'F':
				degree_list.append([(int(date['maxtempF']) + int(date['mintempF'])) / 2, int(date['maxtempF']), int(date['mintempF'])])
			else:
				degree_list.append([(int(date['maxtempC']) + int(date['mintempC'])) / 2, int(date['maxtempC']), int(date['mintempC'])])

	# if not condition:
	# 	return city, dates[0], dates[1], degree_list
	# else:
	# 	return city, dates[0], dates[1], degree_list, condition_list
	return city, dates[0], dates[1], degree_list, condition_list

def weather_time_period(parameters, wwo):

	address = parameters.get('address')
	date_time = parameters.get('date-time')
	unit = parameters.get('unit')
	condition = parameters.get('condition')
	city = address.get('city')
	time_period = date_time.get('time-period')

	degree_list = []
	condition_list = []
	hours = time_period.split('/')
	weather = wwo['weather'][0]
	start_time = hours[0]
	end_time = hours[1]

	if datetime.strptime(start_time, '%H:%M:%S').hour == 0:
		params_hour_start = str(datetime.strptime(start_time, '%H:%M:%S').hour)
	else:
		params_hour_start = str(datetime.strptime(start_time, '%H:%M:%S').hour) + '00'

	if datetime.strptime(end_time, '%H:%M:%S').hour == 0:
		params_hour_end = str(datetime.strptime(end_time, '%H:%M:%S').hour)
	else:
		params_hour_end = str(datetime.strptime(end_time, '%H:%M:%S').hour) + '00'

	for hour_data in weather['hourly']:
		if params_hour_start == hour_data['time'] or params_hour_end == hour_data['time']:
			if condition:
				condition_list.append(hour_data[condition])
			else:
				condition_list.append(hour_data['weatherDesc'][0]["value"].lower())

			if unit and unit == 'C':
				degree_list.append(hour_data['tempC'])
			elif unit and unit == 'F':
				degree_list.append(hour_data['tempF'])
			else:
				degree_list.append(hour_data['tempC'])

	# if not condition:
	# 	return city, hours[0], hours[1], degree_list
	# else:
	# 	return city, hours[0], hours[1], degree_list, condition_list
	return city, hours[0], hours[1], degree_list, condition_list

def weather_current(parameters, wwo):
	print parameters
	address = parameters.get('address')
	unit = parameters.get('unit')
	condition = parameters.get('condition')
	city = address.get('city')
	f_countries = ['BS', 'BZ', 'KY', 'US']

	if unit and unit == 'C':
		temp = wwo['current_condition'][0]['temp_C']
		unit = 'celsius'
	elif unit and unit == 'F' or address['country_code'] in f_countries:
		temp = wwo['current_condition'][0]['temp_F']
		unit = 'fahrenheit'
	else:
		temp = wwo['current_condition'][0]['temp_C']
		unit = 'celsius'
	desc = wwo['current_condition'][0]['weatherDesc'][0]['value']

	if not condition:
		return city, int(temp), desc, unit
	else:
		time = wwo['current_condition'][0]["observation_time"]
		time = py_time.strptime(time, '%I:%M %p')
		if time.tm_hour != 0:
			time = str(time.tm_hour) + '00'
		else:
			time = str(time.tm_hour)
		for hour in wwo["weather"][0]['hourly']:
			if hour['time'] == time:
				condition = hour[condition]
		return city, int(temp), desc, int(condition), unit