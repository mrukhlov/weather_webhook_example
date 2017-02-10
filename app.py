# -*-encoding:utf8-*-

import os

from flask import (
    Flask,
    request,
    make_response,
    jsonify
)

from weather_data_process import (
    weather_current,
    weather_date,
    weather_time,
    weather_date_period,
    weather_time_period,
    date_time_format
)
from weather_entities import (
    winter_activity,
    summer_activity,
    demi_activity,
    condition_dict,
    unsupported,
    cold_weather,
    warm_weather,
    hot_weather,
    unknown_weather,
    rain,
    snow,
    sun
)
from weather_response import (
    weather_response_current,
    weather_response_date,
    weather_response_time_period,
    weather_response_date_period,
    weather_response_time,
    weather_response_date_time,
    weather_response_activity,
    weather_response_condition,
    weather_response_outfit,
    weather_response_temperature
)
from wwo_api import wwo_weather_get

app = Flask(__name__)
log = app.logger

apikey = '7UmuyhWz6qteGNoQRusNzXA9M0Ccwlf8'

unit_global = 'F'


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
    # parameters = address_getter(req['result']['parameters'])
    parameters = req['result']['parameters']
    address = parameters.get('address')
    city = None
    if address:
        city = address.get('city')
    if parameters.get('date-time'):
        parameters = date_time_format(parameters)
    date_time = parameters.get('date-time')
    unit = parameters.get('unit')
    if not unit:
        if len(unit_global) > 0:
            parameters['unit'] = unit_global
    # context = req['contexts']

    if city:

        wwo = wwo_weather_get(parameters)
        error = wwo.get('error')

        if not error:
            '''if we get date and time parameters'''
            if date_time:

                date = date_time.get('date')
                time = date_time.get('time')
                date_and_time = date_time.get('date-and-time')
                date_period = date_time.get('date-period')
                time_period = date_time.get('time-period')

                if time or date_and_time:
                    city, date, time, temp, unit, desc, weather_data = weather_time(parameters, wwo)
                    if time:
                        resp = weather_response_time(city, date, time, temp, unit, desc)
                    else:
                        resp = weather_response_date_time(city, date, time, temp, unit, desc)
                elif date:
                    city, date, temp, unit, min_temp, max_temp, weather_data, desc = \
                        weather_date(parameters, wwo)
                    resp = weather_response_date(city, date, temp, unit, min_temp, max_temp, desc)
                elif date_period:
                    city, date_start, date_end, degree_list, condition_list, weather_data = \
                        weather_date_period(parameters, wwo)
                    resp = weather_response_date_period(
                        city, date_start, date_end, degree_list, condition_list)
                elif time_period:
                    city, time_start, time_end, degree_list, condition_list, weather_data = \
                        weather_time_period(parameters, wwo)
                    resp = weather_response_time_period(
                        city, time_start, time_end, degree_list, condition_list)
            else:
                '''else we just return current conditions'''
                city, temp, desc, unit, weather_data = weather_current(parameters, wwo)
                resp = weather_response_current(city, temp, desc, unit)
        else:
            resp = error
    else:
        resp = 'Please specify city.'
    return {"speech": resp, "displayText": resp}


def weather_activity(req):
    # parameters = address_getter(req['result']['parameters'])
    parameters = req['result']['parameters']
    address = parameters.get('address')
    city = None
    if address:
        city = address.get('city')
    if parameters.get('date-time'):
        parameters = date_time_format(parameters)
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
                date_and_time = date_time.get('date-and-time')
                date_period = date_time.get('date-period')
                time_period = date_time.get('time-period')

                if time or date_and_time:
                    city, date, time, temp, unit, desc, weather_data = weather_time(parameters, wwo)
                    if time:
                        weather_resp = weather_response_time(city, date, time, temp, unit, desc)
                    else:
                        weather_resp = weather_response_date_time(city, date, time, temp, unit, desc)
                elif date:
                    city, date, temp, unit, min_temp, max_temp, weather_data, desc = \
                        weather_date(parameters, wwo)
                    weather_resp = weather_response_date(
                        city, date, temp, unit, min_temp, max_temp, desc)
                elif date_period:
                    city, date_start, date_end, degree_list, condition_list, weather_data = \
                        weather_date_period(parameters, wwo)
                    weather_resp = weather_response_date_period(
                        city, date_start, date_end, degree_list, condition_list)
                    temp = sum([i[0] for i in degree_list]) / len(degree_list)
                elif time_period:
                    city, time_start, time_end, degree_list, condition_list, weather_data = \
                        weather_time_period(parameters, wwo)
                    weather_resp = weather_response_time_period(
                        city, time_start, time_end, degree_list, condition_list)
                    temp = sum([i[0] for i in degree_list]) / len(degree_list)
                resp = str(weather_resp) + ' ' + str(
                    weather_response_activity(activity, temp, winter_activity, summer_activity, demi_activity))
            else:
                '''else we just return current conditions'''
                city, temp, desc, unit, weather_data = weather_current(parameters, wwo)
                weather_resp = weather_response_current(city, temp, desc, unit)
                resp = str(weather_resp) + ' ' + str(
                    weather_response_activity(activity, temp, winter_activity, summer_activity, demi_activity))
        else:
            resp = error
    else:
        resp = 'Please specify location.'
    return {"speech": resp, "displayText": resp}


def weather_condition(req):
    # parameters = address_getter(req['result']['parameters'])
    parameters = req['result']['parameters']
    address = parameters.get('address')
    city = None
    if address:
        city = address.get('city')
    if parameters.get('date-time'):
        parameters = date_time_format(parameters)
    date_time = parameters.get('date-time')
    condition = parameters.get('condition')
    unit = parameters.get('unit')
    if not unit:
        if len(unit_global) > 0:
            parameters['unit'] = unit_global
    condition_list = []
    if condition in unsupported:
        error = 'Unsupported condition'
        return {"speech": error, "displayText": error}
    else:
        parameters['condition_original'] = condition
        parameters['condition'] = condition_dict[condition]
        condition_original = parameters['condition_original']

    if city:

        wwo = wwo_weather_get(parameters)
        error = wwo.get('error')

        if not error:
            '''if we get date and time parameters'''
            if date_time:

                date = date_time.get('date')
                time = date_time.get('time')
                date_and_time = date_time.get('date-and-time')
                date_period = date_time.get('date-period')
                time_period = date_time.get('time-period')

                if time or date_and_time:
                    city, date, time, temp, unit, desc, condition, weather_data = weather_time(parameters, wwo)
                    if time:
                        weather_resp = weather_response_time(city, date, time, temp, unit, desc)
                    else:
                        weather_resp = weather_response_date_time(city, date, time, temp, unit, desc)
                if date:
                    city, date, temp, unit, min_temp, max_temp, condition, weather_data, desc = \
                        weather_date(parameters, wwo)
                    weather_resp = weather_response_date(city, date, temp, unit, min_temp, max_temp, desc)
                elif date_period:
                    city, date_start, date_end, degree_list, condition_list, weather_data = \
                        weather_date_period(parameters, wwo)
                    weather_resp = weather_response_date_period(
                        city, date_start, date_end, degree_list, condition_list, condition_original)
                elif time_period:
                    city, time_start, time_end, degree_list, condition_list, weather_data = \
                        weather_time_period(parameters, wwo)
                    weather_resp = weather_response_time_period(
                        city, time_start, time_end, degree_list, condition_list)
                resp = str(weather_resp) + ' ' + str(
                    weather_response_condition(condition_original, condition, condition_list))
            else:
                '''else we just return current conditions'''
                city, temp, desc, condition, unit, weather_data = weather_current(parameters, wwo)
                weather_resp = weather_response_current(city, temp, desc, unit)
                resp = str(weather_resp) + ' ' + str(
                    weather_response_condition(condition_original, condition))
        else:
            resp = error
    else:
        resp = 'Please specify location.'
    return {"speech": resp, "displayText": resp}


def weather_outfit(req):
    # parameters = address_getter(req['result']['parameters'])
    parameters = req['result']['parameters']
    address = parameters.get('address')
    city = None
    if address:
        city = address.get('city')
    if parameters.get('date-time'):
        parameters = date_time_format(parameters)
    date_time = parameters.get('date-time')
    outfit = parameters.get('outfit')

    unit = parameters.get('unit')
    if not unit:
        if len(unit_global) > 0:
            parameters['unit'] = unit_global

    if outfit:
        if outfit in cold_weather or outfit in warm_weather or outfit in hot_weather or outfit in unknown_weather:
            if outfit in cold_weather:
                temp_limit = -5
            if outfit in warm_weather:
                temp_limit = 10
            if outfit in hot_weather or outfit in unknown_weather:
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
    else:
        resp = 'You forgot to specify your outfit.'
        return {"speech": resp, "displayText": resp}
    condition = parameters.get('condition')

    if city:

        wwo = wwo_weather_get(parameters)
        error = wwo.get('error')

        if not error:
            '''if we get date and time parameters'''
            if date_time:

                date = date_time.get('date')
                time = date_time.get('time')
                date_and_time = date_time.get('date-and-time')
                date_period = date_time.get('date-period')
                time_period = date_time.get('time-period')

                if time or date_and_time:
                    if outfit in rain or outfit in snow or outfit in sun:
                        city, date, time, temp, unit, desc, condition, weather_data = \
                            weather_time(parameters, wwo)
                    else:
                        city, date, time, temp, unit, desc, weather_data = weather_time(parameters, wwo)

                    if time:
                        weather_resp = weather_response_time(city, date, time, temp, unit, desc)
                    else:
                        weather_resp = weather_response_date_time(city, date, time, temp, unit, desc)
                elif date:
                    if outfit in rain or outfit in snow or outfit in sun:
                        city, date, temp, unit, min_temp, max_temp, condition, weather_data, desc = \
                            weather_date(parameters, wwo)
                    else:
                        city, date, temp, unit, min_temp, max_temp, weather_data, desc = \
                            weather_date(parameters, wwo)
                    weather_resp = weather_response_date(
                        city, date, temp, unit, min_temp, max_temp, desc)
                elif date_period:
                    city, date_start, date_end, degree_list, condition_list, weather_data = \
                        weather_date_period(parameters, wwo)
                    weather_resp = weather_response_date_period(
                        city, date_start, date_end, degree_list, condition_list, condition_original)
                    temp = sum([i[0] for i in degree_list]) / len(degree_list)
                elif time_period:
                    city, time_start, time_end, degree_list, condition_list, weather_data = \
                        weather_time_period(parameters, wwo)
                    weather_resp = weather_response_time_period(
                        city, time_start, time_end, degree_list, condition_list)
                    temp = sum([i[0] for i in degree_list]) / len(degree_list)
                resp = str(weather_resp) + ' ' + str(
                    weather_response_outfit(
                        outfit, rain, snow, sun, condition, temp, temp_limit, condition_original))
            else:
                '''else we just return current conditions'''
                if condition:
                    city, temp, desc, condition, unit, weather_data = \
                        weather_current(parameters, wwo)
                else:
                    city, temp, desc, unit, weather_data = weather_current(parameters, wwo)
                weather_resp = weather_response_current(city, temp, desc, unit)
                resp = str(weather_resp) + ' ' + str(
                    weather_response_outfit(
                        outfit, rain, snow, sun, condition, temp, temp_limit, condition_original))
        else:
            resp = error
    else:
        resp = 'Please specify city.'
    return {"speech": resp, "displayText": resp}


def weather_temperature(req):
    # parameters = address_getter(req['result']['parameters'])
    parameters = req['result']['parameters']
    address = parameters.get('address')
    city = None
    if address:
        city = address.get('city')
    if parameters.get('date-time'):
        parameters = date_time_format(parameters)
    date_time = parameters.get('date-time')
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
                date_and_time = date_time.get('date-and-time')
                date_period = date_time.get('date-period')
                time_period = date_time.get('time-period')

                if time or date_and_time:
                    city, date, time, temp, unit, desc, weather_data = weather_time(parameters, wwo)
                    if time:
                        weather_resp = weather_response_time(city, date, time, temp, unit, desc)
                    else:
                        weather_resp = weather_response_date_time(city, date, time, temp, unit, desc)
                elif date:
                    city, date, temp, unit, min_temp, max_temp, weather_data, desc = \
                        weather_date(parameters, wwo)
                    weather_resp = weather_response_date(
                        city, date, temp, unit, min_temp, max_temp, desc)
                elif date_period:
                    city, date_start, date_end, degree_list, condition_list, weather_data = \
                        weather_date_period(parameters, wwo)
                    weather_resp = weather_response_date_period(
                        city, date_start, date_end, degree_list, condition_list)
                    temp = sum([i[0] for i in degree_list]) / len(degree_list)
                elif time_period:
                    city, time_start, time_end, degree_list, condition_list, weather_data = \
                        weather_time_period(parameters, wwo)
                    weather_resp = weather_response_time_period(
                        city, time_start, time_end, degree_list, condition_list)
                    temp = sum([i[0] for i in degree_list]) / len(degree_list)
                resp = str(weather_resp) + ' ' + str(weather_response_temperature(
                    temperature, temp_limit, temp))
            else:
                '''else we just return current conditions'''
                city, temp, desc, unit, weather_data = weather_current(parameters, wwo)
                weather_resp = weather_response_current(city, temp, desc, unit)
                resp = str(weather_resp) + ' ' + str(weather_response_temperature(
                    temperature, temp_limit, temp))
        else:
            resp = error
    else:
        resp = 'Please specify city.'
    return {"speech": resp, "displayText": resp}


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
