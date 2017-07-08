import requests
import hashlib
import json
import os

def getNestTemp( sensor):

	url = "https://developer-api.nest.com/"
	token = os.environ['NEST_TOKEN']

	headers = {'Authorization': 'Bearer {0}'.format(token), 'Content-Type': 'application/json'} # Update with your token

	initial_response = requests.get(url, headers=headers, allow_redirects=False)
	if initial_response.status_code == 307:
    		initial_response = requests.get(initial_response.headers['Location'], headers=headers, allow_redirects=False)


	temp = json.loads(initial_response.text)
	for t in temp['devices']['thermostats']:
		if( temp['devices']['thermostats'][t]['device_id'] == sensor ):
			print temp['devices']['thermostats'][t]['device_id']
			print temp['devices']['thermostats'][t]['ambient_temperature_c']
			return float(temp['devices']['thermostats'][t]['ambient_temperature_c']);
