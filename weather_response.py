from datetime import datetime

def weather_response_current(city, temp, desc, unit):
	res = 'Now in %s is %s and %s.' % (city, temp, desc)
	return res

def weather_response_time():
	pass

def weather_response_date(city, date, temp, unit, min_temp, max_temp):
	# res = 'Weather in %s on %s will be %s degrees %s. Minimum %s degrees and maximum %s.' % (city, date, temp, unit, min_temp, max_temp)
	if datetime.today().day == datetime.strptime(date, '%Y-%m-%d'):
		res = 'Today in %s it will be between %s  and %s.' % (city, min_temp, max_temp)
	elif datetime.strptime(date, '%Y-%m-%d').day - datetime.today().day == 1 :
		res = 'Tomorrow it will be between %s and %s.' % (min_temp, max_temp)
	else:
		res = 'On %s in %s it will be %s, with a low of %s and a high of %s.' % (date, city, temp, min_temp, max_temp)
	return res

def weather_response_time_period():
	pass

def weather_response_date_period(*args):
	pass