import requests

apikey = 'ca74181ac9a82057'

def get_location():
	# get city and code
	payload = {'query':'Saint Petersburg'}
	r = requests.get('http://autocomplete.wunderground.com/aq?', params=payload)

	name = r.json()["RESULTS"][0]['name'].split(',')
	city = name[0]
	country = name[1]
	c_code = r.json()["RESULTS"][0]['c']

	return name, c_code

def get_forecast(c_code, city):
	# get forecast
	link = 'http://api.wunderground.com/api/%s/forecast10day/q/%s/%s.json' % (apikey, c_code, city)
	r = requests.get(link)
	print r.text

