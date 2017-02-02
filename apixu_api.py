import requests

apikey = '4cb13f4977874380a9e124558170102'
link = 'http://api.apixu.com/v1'

params = {'key':apikey, 'q':'Moscow', 'days':'1'}
r = requests.get(link+'/forecast.json', params=params)

for i in r.json():
	print i

for i in r.json()['forecast']['forecastday'][0]['hour']:
	print i