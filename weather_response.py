# -*- coding:utf8 -*-

import random
from datetime import datetime
from weather_strings_list import (
    _STRING_LIST_YES,
    _STRING_LIST_NO,
    _STRING_LIST_COLD,
    _STRING_LIST_CHILLY,
    _STRING_LIST_WARM,
    _STRING_LIST_HOT,
    _STRING_WEATHER_CURRENT,
    _STRING_WEATHER_DATE,
    _STRING_WEATHER_WEEKDAY,
    _STRING_WEATHER_DATE_TIME,
    _STRING_WEATHER_TIME_PERIOD,
    _STRING_WEATHER_TIME_PERIOD_DEFINED,
    _STRING_WEATHER_DATE_PERIOD_WEEKEND,
    _STRING_WEATHER_DATE_PERIOD,
    _STRING_WEATHER_ACTIVITY_YES,
    _STRING_WEATHER_ACTIVITY_NO,
    _STRING_RESPONSE_WEATHER_CONDITION,
    _STRING_RESPONSE_WEATHER_OUTFIT,
)

def weather_response_current(weather):
    temp = str(weather.temp) + '°F'
    output_string = random.choice(_STRING_WEATHER_CURRENT)
    res = output_string.format(place=weather.city, temperature=temp, condition=weather.desc.lower())
    return res


def weather_response_time(weather):
    temp = str(weather.temp) + '°F'
    time = datetime.strftime(datetime.strptime(weather.time, '%H:%M:%S'), '%H:%M')
    output_string = random.choice(_STRING_WEATHER_DATE_TIME)
    res = output_string.format(place=weather.city, time=time, temperature=temp, condition=weather.desc.lower(), day='Today')
    return res


def weather_response_date_time(weather):
    temp = str(weather.temp) + '°F'
    time = datetime.strftime(datetime.strptime(weather.time, '%H:%M:%S'), '%H:%M')
    date = datetime.strptime(weather.date, '%Y-%m-%d')
    if date == datetime.today().day or date == - datetime.today().day == 1:
      if datetime.today().day == date.day:
        day = 'Today'
      if date.day - datetime.today().day == 1:
        day = 'Tomorrow'
    else:
      if date.day - datetime.today().day < 8:
        weekday = date.isoweekday()
        weekday_str = datetime.strftime(date, '%A').lower()
        if weekday == 6:
            day = 'Saturday'
        elif weekday == 7:
            day = 'Sunday'
        else:
            day = weekday_str
      else:
        date = datetime.strftime(date, '%B, %d')
        day = date

    output_string = random.choice(_STRING_WEATHER_DATE_TIME)
    res = output_string.format(
      place=weather.city, time=time, temperature=temp, condition=weather.desc.lower(), day=day.capitalize()
    )
    return res


def weather_response_date(weather):
    temp = str(weather.temp) + '°F'
    min_temp = str(weather.min_temp) + '°F'
    max_temp = str(weather.max_temp) + '°F'
    if datetime.today().day == datetime.strptime(weather.date, '%Y-%m-%d').day or \
                    datetime.strptime(weather.date, '%Y-%m-%d').day - datetime.today().day == 1:
      if datetime.today().day == datetime.strptime(weather.date, '%Y-%m-%d').day:
        day = 'Today'
      if datetime.strptime(weather.date, '%Y-%m-%d').day - datetime.today().day == 1:
        day = 'Tomorrow'
      output_string = random.choice(_STRING_WEATHER_DATE)
      res = output_string.format(place=weather.city, day=day, temperature=temp, condition=weather.desc.lower())
    else:
      if datetime.strptime(weather.date, '%Y-%m-%d').day - datetime.today().day < 8:
        weekday = datetime.strptime(weather.date, '%Y-%m-%d').isoweekday()
        weekday_str = datetime.strftime(datetime.strptime(weather.date, '%Y-%m-%d'), '%A').lower()
        if weekday == 6 or weekday == 7:
            if weekday == 6:
              output_string = random.choice(_STRING_WEATHER_WEEKDAY)
              res = output_string.format(
                place=weather.city,
                condition=weather.desc.lower(),
                temperature=temp,
                date='Saturday'
              )
            else:
              output_string = random.choice(_STRING_WEATHER_WEEKDAY)
              res = output_string.format(
                place=weather.city,
                condition=weather.desc.lower(),
                temperature=temp,
                date='Sunday'
              )
        else:
            output_string = random.choice(_STRING_WEATHER_WEEKDAY)
            res = output_string.format(
              date=weekday_str.capitalize(),
              place=weather.city,
              condition=weather.desc.lower(),
              temperature=temp
            )
      else:
        date = datetime.strftime(datetime.strptime(weather.date, '%Y-%m-%d'), '%B, %d')
        output_string = random.choice(_STRING_WEATHER_WEEKDAY)
        res = output_string.format(
            date=date, place=weather.city, condition=weather.desc.lower(), temperature=temp
        )
    return res


def weather_response_time_period(weather):
    temp = str(weather.degree_list[0]) + '°F'
    hour_start = datetime.strptime(weather.time_start, '%H:%M:%S').hour
    hour_end = datetime.strptime(weather.time_end, '%H:%M:%S').hour
    if hour_start == 12 and hour_end == 16 or \
                    hour_start == 0 and hour_end == 8 or \
                    hour_start == 16 and hour_end == 23 or \
                    hour_start == 8 and hour_end == 12:
      if hour_start == 12 and hour_end == 16:
        time_period = 'afternoon'
      elif hour_start == 0 and hour_end == 8:
        time_period = 'night'
      elif hour_start == 16 and hour_end == 23:
        time_period = 'tonight'
      elif hour_start == 8 and hour_end == 12:
        time_period = 'morning'

      output_string = random.choice(_STRING_WEATHER_TIME_PERIOD_DEFINED)
      res = output_string.format(
        place=weather.city, time_period=time_period, temperature=temp, condition=weather.condition_list[0]
      )
    else:
      res = random.choice(_STRING_WEATHER_TIME_PERIOD).format\
        (
            condition=str(weather.condition_list[0]),
            city=weather.city,
            temp=temp,
            time_start=weather.time_start,
            time_end=weather.time_end
        )
    return res


def weather_response_date_period(weather):
    if datetime.strptime(weather.date_start, '%Y-%m-%d').isoweekday() == 6 and \
              datetime.strptime(weather.date_end, '%Y-%m-%d').isoweekday() == 7:
      if isinstance(weather.condition_list[0], list):
        condition_sun = weather.condition_list[0][0]
        condition_sat = weather.condition_list[1][0]
      else:
        condition_sun = weather.condition_list[0]
        condition_sat = weather.condition_list[1]
      sun_temp_min, sun_temp_max = str(weather.degree_list[0][2]) + '°F', str(weather.degree_list[0][1]) + '°F'
      sat_temp_min, sat_temp_max = str(weather.degree_list[1][2]) + '°F', str(weather.degree_list[1][1]) + '°F'
      res = random.choice(_STRING_WEATHER_DATE_PERIOD_WEEKEND).format(
          city=weather.city,
          condition_sun=condition_sun,
          sun_temp_min=sun_temp_min,
          sun_temp_max=sun_temp_max,
          condition_sat=condition_sat,
          sat_temp_min=sat_temp_min,
          sat_temp_max=sat_temp_max
        )
    else:
      date_start = datetime.strftime(datetime.strptime(weather.date_start, '%Y-%m-%d'), '%B, %d')
      date_end = datetime.strftime(datetime.strptime(weather.date_end, '%Y-%m-%d'), '%B, %d')
      degree_list_min = str(sum([i[2] for i in weather.degree_list]) / len(weather.degree_list)) + '°F'
      degree_list_max = str(sum([i[1] for i in weather.degree_list]) / len(weather.degree_list)) + '°F'
      if not weather.condition_original:
        condition_original = random.choice(weather.condition_list)
        if isinstance(condition_original, list):
            condition_original = condition_original[0]
      res = random.choice(_STRING_WEATHER_DATE_PERIOD).format(
            date_start=date_start,
            date_end=date_end,
            city=weather.city,
            condition=condition_original,
            degree_list_min=degree_list_min,
            degree_list_max=degree_list_max
        )
    return res


def weather_response_activity(activity, temp, winter_activity, summer_activity, demi_activity):
    if activity in demi_activity:
      resp = random.choice(_STRING_WEATHER_ACTIVITY_YES).format(activity=activity)
    elif activity in winter_activity:
      if temp <= 32:
        resp = random.choice(_STRING_WEATHER_ACTIVITY_YES).format(activity=activity)
      else:
        resp = random.choice(_STRING_WEATHER_ACTIVITY_NO).format(activity=activity)
    elif activity in summer_activity:
      if temp >= 50:
        resp = random.choice(_STRING_WEATHER_ACTIVITY_YES).format(activity=activity)
      else:
        resp = random.choice(_STRING_WEATHER_ACTIVITY_NO).format(activity=activity)

    return resp


def weather_response_condition(condition_original, condition, condition_list=None):
    if condition_list:
      condition = random.choice(condition_list)
    if isinstance(condition, list):
      condition = condition[1]
    resp = random.choice(_STRING_RESPONSE_WEATHER_CONDITION).format(
        condition_original=condition_original,
        condition=condition
    )
    return resp


def weather_response_outfit(
      outfit, rain, snow, sun, condition, temp, temp_limit, condition_original, condition_list=None
):
    if outfit in rain or outfit in snow or outfit in sun:
      string_list = _STRING_LIST_YES if condition > 50 else _STRING_LIST_NO
      answer = random.choice(string_list)

      if condition_list:
        condition = random.choice(condition_list)[1]
      resp = random.choice(_STRING_RESPONSE_WEATHER_OUTFIT).format(
          condition_original=condition_original,
          condition=condition,
          answer=answer
      )
    else:
      if temp_limit[1] >= 32:
        resp = _STRING_LIST_NO if temp <= temp_limit else _STRING_LIST_YES
        resp = random.choice(resp)
      else:
        resp = _STRING_LIST_NO if temp >= temp_limit else _STRING_LIST_YES
        resp = random.choice(resp)

    return resp


def weather_response_temperature(temperature, temp_limit, temp):
    if not temperature:
      resp = ''
    else:
      if temp_limit == 77:
        resp = _STRING_LIST_HOT if temp >= temp_limit else _STRING_LIST_WARM
        resp = random.choice(resp)
      elif temp_limit == 59:
        resp = _STRING_LIST_WARM if temp >= temp_limit else _STRING_LIST_CHILLY
        resp = random.choice(resp)
      elif temp_limit == 41:
        resp = _STRING_LIST_CHILLY if temp >= temp_limit else _STRING_LIST_COLD
        resp = random.choice(resp)
      elif temp_limit == 23:
        resp = random.choice(_STRING_LIST_COLD)

    return resp
