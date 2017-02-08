from datetime import datetime
import random

def weather_response_current(city, temp, desc, unit):
	res = 'Now in %s is %s degrees %s and %s.' % (city, temp, unit, desc)
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
		rand = random.randrange(len(degree_list))
		res = 'This %s will be %s and %s.' % (time_period, degree_list[rand], condition_list[rand])
	else:
		res = 'The weather in %s on period from %s till %s will be: %s.' % (city, time_start, time_end, str(degree_list))
	return res

def weather_response_date_period(city, date_start, date_end, degree_list, condition_list):
	if datetime.strptime(date_start, '%Y-%m-%d').isoweekday() == 6 and datetime.strptime(date_end, '%Y-%m-%d').isoweekday() == 7:
		res = 'On Saturday in %s it will be %s, with temperatures from %s to %s. And Sunday should be %s, with a low of %s and a high of %s.' % (city, condition_list[0], degree_list[0][1], degree_list[0][2], condition_list[1], degree_list[1][1], degree_list[1][2])
	else:
		res = 'The weather in %s on period from %s till %s will be: %s' % (city, date_start, date_end, str(degree_list))
	return res