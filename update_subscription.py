import requests
import json

file = open('res/hub_params.json')
update_params = json.load(file)
file.close()

url = 'https://pubsubhubbub.appspot.com'

x = requests.post(url, data = update_params)