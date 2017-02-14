# -*- coding:utf8 -*-

from datetime import datetime
import time as py_time
from country_codes import codes
import requests

def address_getter(parameters):

    address = parameters.get('address')

    if address:
        city = address.get('city')
        country = address.get('country')
        if country and country == 'Russian Federation': country = 'Russia'
        if not city:
            send_url = 'http://ipinfo.io'
            request = requests.get(send_url)
            if codes[request.json().get('country')] == country:
                city = request.json().get('city')
                if city:
                    parameters['address']['city'] = city
    else:
        parameters['address'] = {}
        send_url = 'http://ipinfo.io'
        request = requests.get(send_url)
        city = request.json().get('city')
        country = codes[request.json().get('country')]
        if city:
            parameters['address']['city'] = city
        if country:
            parameters['address']['country'] = country
            parameters['address']['country_code'] = request.json().get('country')

    return parameters

def date_time_format(parameters):
    date_time_date = parameters['date-time']
    try:
        if date_time_date.find('/') > -1:
            if date_time_date.find(':') > -1:
                parameters['date-time'] = {'time-period':date_time_date}
            elif date_time_date.find('-') > -1:
                parameters['date-time'] = {'date-period':date_time_date}
        else:
            if date_time_date.find('T') > -1:
                parameters['date-time'] = {'date-and-time':date_time_date}
            elif date_time_date.find(':') > -1:
                parameters['date-time'] = {'time':date_time_date}
            elif date_time_date.find('-') > -1:
                parameters['date-time'] = {'date':date_time_date}
    except AttributeError:
        parameters.pop('date-time', None)
        parameters['error'] = 'Platform error.'
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
    desc = weather["hourly"][6]["weatherDesc"][0]["value"].lower()

    weather_data = {
        'weather': {
            "maxtempC": weather["maxtempC"],
            "maxtempF": weather["maxtempF"],
            "mintempC": weather["mintempC"],
            "mintempF": weather["mintempF"],
            "tempC": (int(weather["maxtempC"]) + int(weather["mintempC"])) / 2,
            "tempF": (int(weather["maxtempF"]) + int(weather["mintempF"])) / 2,
        },
        "date": date,
        "location": wwo["request"][0]["query"],
        "logo": weather["hourly"][6]["weatherIconUrl"][0]["value"],
        "description": weather["hourly"][6]["weatherDesc"][0]["value"]
    }

    if not condition:
        return city, date, int(temp), unit, min_temp, max_temp, weather_data, desc
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

        return city, date, int(temp), unit, min_temp, max_temp, int(condition), weather_data, desc

def weather_time(parameters, wwo):

    address = parameters.get('address')
    date_time = parameters.get('date-time')
    unit = parameters.get('unit')
    condition = parameters.get('condition')

    city = address.get('city')
    date_and_time = date_time.get('date-and-time')
    if date_and_time:
        time = datetime.strftime(datetime.strptime(date_and_time, '%Y-%m-%dT%H:%M:%SZ'), '%H:%M:%S')
    else:
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

            weather_data_tempC = hour_data['tempC']
            weather_data_tempF = hour_data['tempF']
            weather_data_logo = hour_data["weatherIconUrl"][0]["value"]
            weather_data_desc = hour_data["weatherDesc"][0]["value"].lower()


    weather_data = {
        'weather': {
            "maxtempC": weather["maxtempC"],
            "maxtempF": weather["maxtempF"],
            "mintempC": weather["mintempC"],
            "mintempF": weather["mintempF"],
            "tempC": weather_data_tempC,
            "tempF": weather_data_tempF,
        },
        "date": date,
        "location": wwo["request"][0]["query"],
        "logo": weather_data_logo,
        "description": weather_data_desc
    }

    if not condition:
        return city, date, time, int(temp), unit, weather_data_desc, weather_data
    else:
        return city, date, time, int(temp), unit, weather_data_desc, int(condition), weather_data

def weather_date_period(parameters, wwo):

    address = parameters.get('address')
    date_time = parameters.get('date-time')
    unit = parameters.get('unit')
    condition = parameters.get('condition')

    date_period = date_time.get('date-period')
    city = address.get('city')

    degree_list = []
    condition_list = []
    weather_data = {}
    dates = date_period.split('/')
    weather = wwo['weather']
    for date in weather:
        if datetime.strptime(date['date'], '%Y-%m-%d') >= \
                datetime.strptime(dates[0], '%Y-%m-%d') or \
                        datetime.strptime(date['date'], '%Y-%m-%d') <= \
                        datetime.strptime(dates[1], '%Y-%m-%d'):
            for hour_data in date['hourly']:
                if hour_data['time'] == '1200':
                    if condition:
                        condition_list.append(hour_data[condition])
                    else:
                        condition_list.append(hour_data['weatherDesc'][0]["value"].lower())

                    weather_data_logo = hour_data['weatherIconUrl'][0]["value"]
                    weather_data_desc = hour_data['weatherDesc'][0]["value"].lower()

            weather_data_tempC = (int(date['maxtempC']) + int(date['mintempC'])) / 2
            weather_data_tempF = (int(date['maxtempF']) + int(date['mintempF'])) / 2
            if unit and unit == 'C':
                degree_list.append(
                    [weather_data_tempC, int(date['maxtempC']), int(date['mintempC'])]
                )
            elif unit and unit == 'F':
                degree_list.append(
                    [weather_data_tempF, int(date['maxtempF']), int(date['mintempF'])]
                )
            else:
                degree_list.append(
                    [weather_data_tempC, int(date['maxtempC']), int(date['mintempC'])]
                )

            weather_data[date['date']] = {
                'weather': {
                    "maxtempC": weather[0]["maxtempC"],
                    "maxtempF": weather[0]["maxtempF"],
                    "mintempC": weather[0]["mintempC"],
                    "mintempF": weather[0]["mintempF"],
                    "tempC": weather_data_tempC,
                    "tempF": weather_data_tempF,
                },
                "date": date,
                "location": wwo["request"][0]["query"],
                "logo": weather_data_logo,
                "description": weather_data_desc
            }

    return city, dates[0], dates[1], degree_list, condition_list, weather_data

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
    date = weather['date']
    start_time = hours[0]
    end_time = hours[1]
    weather_data = {}

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

            weather_data_tempC = hour_data['tempC']
            weather_data_tempF = hour_data['tempF']
            weather_data_logo = hour_data["weatherIconUrl"][0]["value"]
            weather_data_desc = hour_data["weatherDesc"][0]["value"].lower()

            if unit and unit == 'C':
                degree_list.append(hour_data['tempC'])
            elif unit and unit == 'F':
                degree_list.append(hour_data['tempF'])
            else:
                degree_list.append(hour_data['tempC'])

            weather_data[hour_data['time']] = {
                'weather': {
                    "maxtempC": weather["maxtempC"],
                    "maxtempF": weather["maxtempF"],
                    "mintempC": weather["mintempC"],
                    "mintempF": weather["mintempF"],
                    "tempC": weather_data_tempC,
                    "tempF": weather_data_tempF,
                },
                "date": date,
                "location": wwo["request"][0]["query"],
                "logo": weather_data_logo,
                "description": weather_data_desc
            }

    return city, hours[0], hours[1], degree_list, condition_list, weather_data

def weather_current(parameters, wwo):

    address = parameters.get('address')
    unit = parameters.get('unit')
    condition = parameters.get('condition')
    city = address.get('city')
    f_countries = ['BS', 'BZ', 'KY', 'US']
    country_code = address.get('country_code')
    weather = wwo['weather'][0]
    date = weather['date']

    if unit and unit == 'C':
        temp = wwo['current_condition'][0]['temp_C']
        unit = 'celsius'
    elif unit and unit == 'F' or country_code in f_countries:
        temp = wwo['current_condition'][0]['temp_F']
        unit = 'fahrenheit'
    else:
        temp = wwo['current_condition'][0]['temp_C']
        unit = 'celsius'
    desc = wwo['current_condition'][0]['weatherDesc'][0]['value'].lower()

    weather_data = {
        'weather': {
            "maxtempC": weather["maxtempC"],
            "maxtempF": weather["maxtempF"],
            "mintempC": weather["mintempC"],
            "mintempF": weather["mintempF"],
            "tempC": (int(weather["maxtempC"]) + int(weather["mintempC"])) / 2,
            "tempF": (int(weather["maxtempF"]) + int(weather["mintempF"])) / 2,
        },
        "date": date,
        "location": wwo["request"][0]["query"],
        "logo": weather["hourly"][6]["weatherIconUrl"][0]["value"],
        "description": weather["hourly"][6]["weatherDesc"][0]["value"].lower()
    }
    if not condition:
        return city, int(temp), desc, unit, weather_data
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
        return city, int(temp), desc, int(condition), unit, weather_data
