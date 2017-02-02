import requests

apikey = '7UmuyhWz6qteGNoQRusNzXA9M0Ccwlf8'

def get_location_id(location, apikey, country=None):
	payload = {'apikey': apikey, 'q': location}
	r = requests.get('http://dataservice.accuweather.com/locations/v1/search?', params=payload)
	id = None
	if country:
		for entry in r.json():
			if entry['Country']["LocalizedName"] == country and entry['LocalizedName'] == location:
				id = entry['Key']
	else:
		for entry in r.json():
			if entry['LocalizedName'] == location or entry['LocalizedName'].find(location) > 0:
				id = r.json()[0].get('Key')

	return id

def accu_weather_get_daily(city, apikey, country=None):

	location_id = get_location_id(city, apikey, country)
	if location_id:
		payload = {'apikey':apikey, 'metric':'true'}
		link = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/%s?' % (location_id)
		r = requests.get(link, params=payload)
		return r.json()
	else:
		return None

def accu_weather_get_hourly(city, apikey, country=None, unit=None):

	location_id = get_location_id(city, apikey, country)
	if location_id:
		payload = {'apikey':apikey}
		if unit and unit == 'C':
			payload['metric'] = 'true'
		link = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/%s?' % (location_id)
		r = requests.get(link, params=payload)
		return r.json()
	else:
		return None

def accu_weather_get_current(city, apikey, country=None, unit=None):

	location_id = get_location_id(city, apikey, country)
	if location_id:
		payload = {'apikey':apikey}
		if unit and unit == 'C':
			payload['metric'] = 'true'
		link = 'http://dataservice.accuweather.com/currentconditions/v1/%s?' % (location_id)
		r = requests.get(link, params=payload)
		return r.json()
	else:
		return None

# accu_weather_get('moscow')