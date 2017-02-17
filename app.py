# -*- coding:utf8 -*-

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

apikey = '7UmuyhWz6qteGNoQRusNzXA9M0Ccwlf8'
_DEFAULT_TEMP_UNIT = 'F'

_TEMPERATURE_LIMITS = {
    'hot': {'C': 25, 'F': 77},
    'warm': {'C': 15, 'F': 59},
    'chilly': {'C': 15, 'F': 41},
    'cold': {'C': -5, 'F': 23}
}

app = Flask(__name__)
log = app.logger


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    try:
        action = req.get("result").get('action')
    except AttributeError:
        return 'json error'

    print req.get("result").get('resolvedQuery')

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
    city = None
    if address:
        if isinstance(address, dict):
            city = address.get('city')
        else:
            city = ''
    if parameters.get('date-time'):
        parameters = date_time_format(parameters)
        error = parameters.get('error')
        if error:
            return {"speech": error, "displayText": error}
    date_time = parameters.get('date-time')
    unit = parameters.get('unit')
    if not unit:
        if len(_DEFAULT_TEMP_UNIT) > 0:
            parameters['unit'] = _DEFAULT_TEMP_UNIT

    if city:

        wwo = wwo_weather_get(parameters)
        error = wwo.get('error')

        if not error:

            if date_time:

                date = date_time.get('date')
                time = date_time.get('time')
                date_and_time = date_time.get('date-and-time')
                date_period = date_time.get('date-period')
                time_period = date_time.get('time-period')

                if time or date_and_time:
                    weather = weather_time(parameters, wwo)
                    if time:
                        resp = weather_response_time(weather)
                    else:
                        resp = weather_response_date_time(weather)
                elif date:
                    weather = weather_date(parameters, wwo)
                    resp = weather_response_date(weather)
                elif date_period:
                    weather = weather_date_period(parameters, wwo)
                    resp = weather_response_date_period(weather)
                elif time_period:
                    weather = weather_time_period(parameters, wwo)
                    resp = weather_response_time_period(weather)
            else:
                weather = weather_current(parameters, wwo)
                resp = weather_response_current(weather)
        else:
            resp = error
    else:
        resp = 'Please specify city.'
    return {"speech": resp, "displayText": resp}


def weather_activity(req):
    parameters = req['result']['parameters']
    address = parameters.get('address')
    city = None
    if address:
        if isinstance(address, dict):
            city = address.get('city')
        else:
            city = ''
    if parameters.get('date-time'):
        parameters = date_time_format(parameters)
        error = parameters.get('error')
        if error:
            return {"speech": error, "displayText": error}
    date_time = parameters.get('date-time')
    activity = parameters.get('activity')
    if activity not in summer_activity and activity not in winter_activity and activity not in demi_activity:
        resp = 'Unknown activity.'
        return {"speech": resp, "displayText": resp}
    unit = parameters.get('unit')
    if not unit:
        if len(_DEFAULT_TEMP_UNIT) > 0:
            parameters['unit'] = _DEFAULT_TEMP_UNIT

    if city:

        wwo = wwo_weather_get(parameters)
        error = wwo.get('error')

        if not error:
            
            if date_time:

                date = date_time.get('date')
                time = date_time.get('time')
                date_and_time = date_time.get('date-and-time')
                date_period = date_time.get('date-period')
                time_period = date_time.get('time-period')

                if time or date_and_time:
                    weather = weather_time(parameters, wwo)
                    if time:
                        weather_resp = weather_response_time(weather)
                    else:
                        weather_resp = weather_response_date_time(weather)
                    temp = weather.temp
                elif date:
                    weather = weather_date(parameters, wwo)
                    weather_resp = weather_response_date(weather)
                    temp = weather.temp
                elif date_period:
                    weather = weather_date_period(parameters, wwo)
                    weather_resp = weather_response_date_period(weather)
                    temp = sum([i[0] for i in weather.degree_list]) / len(weather.degree_list)
                elif time_period:
                    weather = weather_time_period(parameters, wwo)
                    weather_resp = weather_response_time_period(weather)
                    temp = sum([i[0] for i in weather.degree_list]) / len(weather.degree_list)
                resp = str(weather_resp) + ' ' + str(
                    weather_response_activity(
                        activity, temp, winter_activity, summer_activity, demi_activity
                    ))
            else:
                weather = weather_current(parameters, wwo)
                weather_resp = weather_response_current(weather)
                resp = str(weather_resp) + ' ' + str(
                    weather_response_activity(
                        activity, weather.temp, winter_activity, summer_activity, demi_activity
                    ))
        else:
            resp = error
    else:
        resp = 'Please specify location.'
    return {"speech": resp, "displayText": resp}


def weather_condition(req):
    parameters = req['result']['parameters']
    address = parameters.get('address')
    city = None
    if address:
        if isinstance(address, dict):
            city = address.get('city')
        else:
            city = ''
    if parameters.get('date-time'):
        parameters = date_time_format(parameters)
        error = parameters.get('error')
        if error:
            return {"speech": error, "displayText": error}
    date_time = parameters.get('date-time')
    condition = parameters.get('condition')
    unit = parameters.get('unit')
    if not unit:
        if len(_DEFAULT_TEMP_UNIT) > 0:
            parameters['unit'] = _DEFAULT_TEMP_UNIT
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
            
            if date_time:

                date = date_time.get('date')
                time = date_time.get('time')
                date_and_time = date_time.get('date-and-time')
                date_period = date_time.get('date-period')
                time_period = date_time.get('time-period')

                if time or date_and_time:
                    weather = weather_time(parameters, wwo)
                    if time:
                        weather_resp = weather_response_time(weather)
                    else:
                        weather_resp = weather_response_date_time(weather)
                if date:
                    weather = weather_date(parameters, wwo)
                    weather_resp = weather_response_date(weather)
                elif date_period:
                    weather = weather_date_period(parameters, wwo)
                    weather_resp = weather_response_date_period(weather)
                elif time_period:
                    weather = weather_time_period(parameters, wwo)
                    weather_resp = weather_response_time_period(weather)
                resp = str(weather_resp) + ' ' + str(
                    weather_response_condition(condition_original, weather.condition, weather.condition_list))
            else:
                weather = weather_current(parameters, wwo)
                weather_resp = weather_response_current(weather)
                resp = str(weather_resp) + ' ' + str(
                    weather_response_condition(condition_original, weather.condition))
        else:
            resp = error
    else:
        resp = 'Please specify location.'
    return {"speech": resp, "displayText": resp}


def weather_outfit(req):
    parameters = req['result']['parameters']
    address = parameters.get('address')
    city = None
    if address:
        if isinstance(address, dict):
            city = address.get('city')
        else:
            city = ''
    if parameters.get('date-time'):
        parameters = date_time_format(parameters)
        error = parameters.get('error')
        if error:
            return {"speech": error, "displayText": error}
    date_time = parameters.get('date-time')
    outfit = parameters.get('outfit')

    unit = parameters.get('unit')
    if not unit:
        if len(_DEFAULT_TEMP_UNIT) > 0:
            parameters['unit'] = _DEFAULT_TEMP_UNIT

    condition_original = None

    if outfit:
        if outfit in cold_weather or outfit in warm_weather or \
        outfit in hot_weather or outfit in unknown_weather:
            if outfit in cold_weather:
                temp_limit = [-5, 23]
            if outfit in warm_weather:
                temp_limit = [10, 50]
            if outfit in hot_weather or outfit in unknown_weather:
                temp_limit = [20, 68]
            condition_original = ''
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
    condition_list = []

    if city:

        wwo = wwo_weather_get(parameters)
        error = wwo.get('error')

        if not error:
            
            if date_time:

                date = date_time.get('date')
                time = date_time.get('time')
                date_and_time = date_time.get('date-and-time')
                date_period = date_time.get('date-period')
                time_period = date_time.get('time-period')

                if time or date_and_time:
                    weather = weather_time(parameters, wwo)
                    if time:
                        weather_resp = weather_response_time(weather)
                    else:
                        weather_resp = weather_response_date_time(weather)
                elif date:
                    weather = weather_date(parameters, wwo)
                    weather_resp = weather_response_date(weather)
                elif date_period:
                    weather = weather_date_period(parameters, wwo)
                    weather_resp = weather_response_date_period(weather)
                    weather.temp = sum([int(i[0]) for i in weather.degree_list]) / len(weather.degree_list)
                elif time_period:
                    weather = weather_time_period(parameters, wwo)
                    weather_resp = weather_response_time_period(weather)
                    weather.temp = sum([int(i[0]) for i in weather.degree_list]) / len(weather.degree_list)
                condition = weather.condition if condition else condition
                resp = str(weather_resp) + ' ' + str(
                    weather_response_outfit(
                        outfit,
                        rain,
                        snow,
                        sun,
                        condition,
                        weather.temp,
                        temp_limit,
                        condition_original,
                        weather.condition_list
                    ))
            else:
                weather = weather_current(parameters, wwo)
                weather_resp = weather_response_current(weather)
                condition = weather.condition if condition else condition
                resp = str(weather_resp) + ' ' + str(
                    weather_response_outfit(
                        outfit, rain, snow, sun, condition, weather.temp, temp_limit, condition_original))
        else:
            resp = error
    else:
        resp = 'Please specify city.'
    return {"speech": resp, "displayText": resp}


def weather_temperature(req):
    parameters = req['result']['parameters']
    address = parameters.get('address')
    city = None
    if address:
        if isinstance(address, dict):
            city = address.get('city')
        else:
            city = ''
    if parameters.get('date-time'):
        parameters = date_time_format(parameters)
        error = parameters.get('error')
        if error:
            return {"speech": error, "displayText": error}
    date_time = parameters.get('date-time')
    temperature = parameters['temperature']

    unit = parameters.get('unit')
    if not unit:
        if len(_DEFAULT_TEMP_UNIT) > 0:
            parameters['unit'] = _DEFAULT_TEMP_UNIT

    temp_limit = _TEMPERATURE_LIMITS[temperature][_DEFAULT_TEMP_UNIT]

    if city:

        wwo = wwo_weather_get(parameters)
        error = wwo.get('error')

        if not error:
            
            if date_time:

                date = date_time.get('date')
                time = date_time.get('time')
                date_and_time = date_time.get('date-and-time')
                date_period = date_time.get('date-period')
                time_period = date_time.get('time-period')

                if time or date_and_time:
                    weather = weather_time(parameters, wwo)
                    if time:
                        weather_resp = weather_response_time(weather)
                    else:
                        weather_resp = weather_response_date_time(weather)
                if date:
                    weather = weather_date(parameters, wwo)
                    weather_resp = weather_response_date(weather)
                elif date_period:
                    weather = weather_date_period(parameters, wwo)
                    weather_resp = weather_response_date_period(weather)
                elif time_period:
                    weather = weather_time_period(parameters, wwo)
                    weather_resp = weather_response_time_period(weather)
                temp = weather.temp if hasattr(weather, 'temp') else weather.degree_list
                resp = str(weather_resp) + ' ' + str(weather_response_temperature(
                    temperature, temp_limit, temp))
            else:
                weather = weather_current(parameters, wwo)
                weather_resp = weather_response_current(weather)
                resp = str(weather_resp) + ' ' + str(weather_response_temperature(
                    temperature, temp_limit, weather.temp
                ))
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
