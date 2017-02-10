from datetime import datetime
import requests

def wwo_weather_get(parameters, number_of_days=1):

    address = parameters.get('address')
    city = address.get('city')

    wwo_data = {
        'key':'436f0dbb6c9b4896be4125125172701',
        'q': city,
        'format': 'json',
        'num_of_days': number_of_days,
        'mca': 'no',
        'lang': 'en',
        # 'fx': 'no',
        'cc': 'yes',
        'tp': '1'
    }

    date_time = parameters.get('date-time')
    if date_time:
        date = date_time.get('date')
        if date:
            today = datetime.today()
            params_day = datetime.strptime(date, '%Y-%m-%d')
            diff = (params_day - today).days
            if diff > 13:
                return {'error':'I couldn\'t find forecast for that far in the future.'}
        date_period = date_time.get('date-period')
        if date_period:
            dates = date_period.split('/')
            today = datetime.today()
            params_day = datetime.strptime(dates[1], '%Y-%m-%d')
            diff_end = (params_day - today).days
            if diff_end > 13:
                return {'error':'I couldn\'t find forecast for that far in the future.'}
            else:
                wwo_data['num_of_days'] = diff_end+1
        time_period = date_time.get('time-period')
        if time_period:
            wwo_data['fx'] = 'yes'
            wwo_data['cc'] = 'no'

        time = date_time.get('time')
        date_and_time = date_time.get('date-and-time')

        if date_and_time:
            date = datetime.strftime(
                datetime.strptime(date_and_time, '%Y-%m-%dT%H:%M:%SZ'),
                '%Y-%m-%d'
            )
            wwo_data['fx'] = 'yes'
            wwo_data['date'] = date
            wwo_data['cc'] = 'no'
        if date:
            wwo_data['fx'] = 'yes'
            wwo_data['date'] = date
        if time:
            wwo_data['fx'] = 'yes'
    else:
        wwo_data['tp'] = '1'

    request = requests.get(
        'http://api.worldweatheronline.com/premium/v1/weather.ashx',
        params=wwo_data
    )

    try:
        json_data = request.json()['data']
        error = json_data.get('error')
        if error:
            json_data = {'error':error[0]['msg']}
    except ValueError:
        json_data = None

    return json_data
