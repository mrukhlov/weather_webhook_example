#-*-encoding:utf8-*-

from datetime import datetime
import random

def weather_response_current(city, temp, desc, unit):
	temp = str(temp)+'°F'
	string_list = [
		'The temperature in {place} now is {temperature} and {condition}.',
		'Right now it\'s {temperature} and {condition} in {place}.',
		'It\'s currently {temperature} and {condition} in {place}.',
		'The temperature in {place} is {temperature} and {condition}.'
	]
	output_string = random.choice(string_list)
	res = output_string.format(place=city, temperature=temp, condition=desc.lower())
	return res

def weather_response_time(city, date, time, temp, unit, desc):
	time = datetime.strftime(datetime.strptime(time, '%H:%M:%S'), '%H:%M')
	string_list = [
		'Today at {time} it will be between {temperature} and {condition}.',
		'Today at {time} you can expect it to be between {temperature} and {condition}.',
		'Today at {time} you can expect {condition}, with temperatures between {temperature}.',
		'Today at {time} will be {condition}, and temperatures will range from {temperature}.',
	]
	output_string = random.choice(string_list)
	res = output_string.format(time=time, temperature=temp, condition=desc.lower())
	return res

def weather_response_date_time(city, date, time, temp, unit, desc):
	time = datetime.strftime(datetime.strptime(time, '%H:%M:%S'), '%H:%M')
	date = datetime.strptime(date, '%Y-%m-%d')
	if date == datetime.today().day or date ==  - datetime.today().day == 1:
		if datetime.today().day == date.day:
			day = 'Today'
		if date.day - datetime.today().day == 1:
			day = 'Tomorrow'
	else:
		if date.day - datetime.today().day < 8:
			weekday = date.isoweekday()
			weekday_str = datetime.strftime(date, '%A').lower()
			if weekday == 6 or weekday == 7:
				if weekday == 6:
					day = 'Saturday'
				else:
					day = 'Sunday'
			else:
				day = weekday_str
		else:
			date = datetime.strftime(date, '%B, %d')
			day = date

	string_list = [
		'{day} in {place} at {time} it will be between {temperature} and {condition}.',
		'{day} in {place} at {time} you can expect it to be between {temperature} and {condition}.',
		'{day} in {place} at {time} you can expect {condition}, with temperatures between {temperature}.',
		'{day} in {place} at {time} will be {condition}, and temperatures will range from {temperature}.',
		'At {time} on {day} in {place} it will be {temperature} and {condition}.'
	]
	output_string = random.choice(string_list)
	res = output_string.format(place=city, time=time, temperature=temp, condition=desc.lower(), day=day.capitalize())
	return res

def weather_response_date(city, date, temp, unit, min_temp, max_temp, desc):
	temp = str(temp) + '°F'
	min_temp = str(min_temp) + '°F'
	max_temp = str(max_temp) + '°F'
	if datetime.today().day == datetime.strptime(date, '%Y-%m-%d').day or datetime.strptime(date, '%Y-%m-%d').day - datetime.today().day == 1:
		if datetime.today().day == datetime.strptime(date, '%Y-%m-%d').day:
			day = 'Today'
		if datetime.strptime(date, '%Y-%m-%d').day - datetime.today().day == 1:
			day = 'Tomorrow'
		string_list = [
			'{day} it will be between {temperature} and {condition}.',
			'{day} you can expect it to be between {temperature} and {condition}.',
			'{day} you can expect {condition}, with temperatures between {temperature}.',
			'{day} will be {condition}, and temperatures will range from {temperature}.',
		]
		output_string = random.choice(string_list)
		res = output_string.format(day=day, temperature=temp, condition=desc.lower())
	else:
		if datetime.strptime(date, '%Y-%m-%d').day - datetime.today().day < 8:
			weekday = datetime.strptime(date, '%Y-%m-%d').isoweekday()
			weekday_str = datetime.strftime(datetime.strptime(date, '%Y-%m-%d'), '%A').lower()
			if weekday == 6 or weekday == 7:
				if weekday == 6:
					string_list = [
						'On Saturday in {place} it will be {condition}, with temperatures from {temperatureMin} to {temperatureMax}.',
						'Saturday in {place} should be {condition}, with temperatures from {temperatureMin} to {temperatureMax}.',
						'Saturday in {place} is expected to be {condition}, with temperatures ranging from {temperatureMin} to {temperatureMax}.',
						'You can expect Saturday in {place} to be {condition}, with temperatures between {temperatureMin} and {temperatureMax}.'
					]
					output_string = random.choice(string_list)
					res = output_string.format(place=city, condition=desc.lower(), temperatureMin=min_temp, temperatureMax=max_temp)
				else:
					string_list = [
						'And Sunday should be {condition}, with a low of {temperatureMin} and a high of {temperatureMax}.',
						'Sunday you can expect {condition}, with temperatures between {temperatureMin} and {temperatureMax}.',
						'On Sunday it will be {condition}, with a low of {temperatureMin} and a high of {temperatureMax}.',
						'Sunday should be {condition}, with temperatures from {temperatureMin} to {temperatureMax}.'
					]
					output_string = random.choice(string_list)
					res = output_string.format(place=city, condition=desc.lower(), temperatureMin=min_temp, temperatureMax=max_temp)
			else:
				string_list = [
					'On {date} it will be {condition}, with a low of {temperatureMin} and a high of {temperatureMax}.',
					'On {date} it\'s expected to be {condition} with temperatures from {temperatureMin} to {temperatureMax}.',
					'The forecast for {date} is {condition}, with temperatures ranging from {temperatureMin} to {temperatureMax}.',
					'{date} is expected to be {condition}, with a low of {temperatureMin} and a high of {temperatureMax}.'
				]
				output_string = random.choice(string_list)
				res = output_string.format(date=weekday_str, place=city, condition=desc.lower(), temperatureMin=min_temp, temperatureMax=max_temp)
		else:
			date = datetime.strftime(datetime.strptime(date, '%Y-%m-%d'), '%B, %d')
			string_list = [
				'On {date} in {place} it will be {condition}, with a low of {temperatureMin} and a high of {temperatureMax}.',
				'On {date} in {place} it\'s expected to be {condition} with temperatures from {temperatureMin} to {temperatureMax}.',
				'The forecast for {date} in {place} is {condition}, with temperatures ranging from {temperatureMin} to {temperatureMax}.',
				'{date} in {place} is expected to be {condition}, with a low of {temperatureMin} and a high of {temperatureMax}.',
			]
			output_string = random.choice(string_list)
			res = output_string.format(date=date, place=city, condition=desc.lower(), temperatureMin=min_temp, temperatureMax=max_temp)
		# res = 'On %s in %s it will be %s, with a low of %s and a high of %s.' % (date, city, temp, min_temp, max_temp)
	return res

def weather_response_time_period(city, time_start, time_end, degree_list, condition_list):
	hour_start = datetime.strptime(time_start, '%H:%M:%S').hour
	hour_end = datetime.strptime(time_end, '%H:%M:%S').hour
	if hour_start == 12 and hour_end == 16 or hour_start == 0 and hour_end == 8 or hour_start == 16 and hour_end == 23 or hour_start == 8 and hour_end == 12:
		if hour_start == 12 and hour_end == 16:
			time_period = 'afternoon'
		if hour_start == 0 and hour_end == 8:
			time_period = 'night'
		if hour_start == 16 and hour_end == 23:
			time_period = 'tonight'
		if hour_start == 8 and hour_end == 12:
			time_period = 'morning'

		string_list = [
			'This {time_period} it will be {temperature} and {condition}.',
			'This {time_period} you can expect {condition}, with temperatures around {temperature}.',
			'Expect a {condition} {time_period}, with temperatures around {temperature}.',
			'It will be {condition} and around {temperature} this {time_period}.',
		]
		output_string = random.choice(string_list)
		res = output_string.format(time_period=time_period, temperature=degree_list[0], condition=condition_list[0])
	else:
		res = 'The weather in %s on period from %s till %s will be: %s.' % (city, time_start, time_end, str(degree_list))
	return res

def weather_response_date_period(city, date_start, date_end, degree_list, condition_list):
	if datetime.strptime(date_start, '%Y-%m-%d').isoweekday() == 6 and datetime.strptime(date_end, '%Y-%m-%d').isoweekday() == 7:
		res = 'On Saturday in %s it will be %s, with temperatures from %s to %s. And Sunday should be %s, with a low of %s and a high of %s.' % (city, condition_list[0], degree_list[0][1], degree_list[0][2], condition_list[1], degree_list[1][1], degree_list[1][2])
	else:
		date_start = datetime.strftime(datetime.strptime(date_start, '%Y-%m-%d'), '%B, %d')
		date_end = datetime.strftime(datetime.strptime(date_end, '%Y-%m-%d'), '%B, %d')
		degree_list_min = sum([i[1] for i in degree_list])/len(degree_list)
		degree_list_max = sum([i[2] for i in degree_list])/len(degree_list)
		# res = 'The weather in %s on period from %s till %s will be: %s' % (city, date_start, date_end, str(degree_list))
		res = 'During period from %s till %s you can expect %s, with a low of %s and a high of %s.' % (date_start, date_end, random.choice(condition_list), degree_list_min, degree_list_max)
	return res

def weather_response_activity(activity, temp, winter_activity, summer_activity, demi_activity):

	if activity in winter_activity or activity in demi_activity:
		if temp < 0:
			resp = 'Perfect conditions for %s!' % (activity)
		else:
			resp = 'Not a best weather for %s.' % (activity)
	elif activity in summer_activity or activity in demi_activity:
		if temp > 0:
			resp = 'Perfect conditions for %s!' % (activity)
		else:
			resp = 'Not a best weather for %s.' % (activity)

	return resp

def weather_response_condition(condition_original, condition):
	resp = 'Chance of %s is %s percent.' % (condition_original, condition)
	return resp

def weather_response_outfit(outfit, rain, snow, sun, condition, temp, temp_limit, condition_original):

	string_list_yes = [
		'Better have it with you, just in case.',
		'It never hurts to be extra prepared.',
		'Better to have it and not need it than to need it and not have it.',
		'Considering the forecast, I\'m going to say yes.'
	]

	string_list_no = [
		'No, you should be fine without it.',
		'I don\'t think that will be necessary.',
		'You can bring it if you like, but I doubt you\'ll need it.',
		'It seems pretty unlikely you\'ll need that.'
	]

	if outfit in rain or outfit in snow or outfit in sun:
		if condition > 50:
			resp = 'Chance of %s is %s percent.' % (condition_original, condition) + ' ' + random.choice(string_list_yes)
		else:
			resp = 'Chance of %s is %s percent.' % (condition_original, condition) + ' ' + random.choice(string_list_no)
	else:
		if temp_limit > 0:
			if temp > temp_limit:
				resp = random.choice(string_list_no)
			else:
				resp = random.choice(string_list_yes)
		else:
			if temp > temp_limit:
				resp = random.choice(string_list_no)
			else:
				resp = random.choice(string_list_yes)

	return resp

def weather_response_temperature(temperature, temp_limit, temp):

	string_list_cold = [
		'Quite cold there.',
		'Pretty freezing, I would say.',
		'Don\'t forget your gloves.'
	]

	string_list_chilly = [
		'Quite chilly.',
		'You\'ll need a jacket for sure.'
	]

	string_list_warm = [
		'Temperature is okay.'
	]

	string_list_hot = [
		'Oh, that\'s hot!',
		'You\'ll definitely need sunscreen.'
	]

	if not temperature:
		resp = ''
	else:
		if temp_limit == 25:
			if temp > temp_limit:
				resp = random.choice(string_list_hot)
			else:
				resp = random.choice(string_list_warm)
		if temp_limit == 15:
			if temp > temp_limit:
				resp = random.choice(string_list_warm)
			else:
				resp = random.choice(string_list_chilly)
		if temp_limit == 5:
			if temp > temp_limit:
				resp = random.choice(string_list_chilly)
			else:
				resp = random.choice(string_list_cold)
		if temp_limit == -5:
			if temp > temp_limit:
				resp = random.choice(string_list_cold)
			else:
				resp = random.choice(string_list_cold)

	return resp