import requests
import json
from datetime import datetime

file = open('res/hub_params.json')
update_params = json.load(file)
file.close()

file2 = open('res/hub_params2.json')
update_params2 = json.load(file2)
file2.close()

url = 'https://pubsubhubbub.appspot.com'

x = requests.post(url, data=update_params)
y = requests.post(url, data=update_params2)
print("Updated subsciptions: {}".format(datetime.now()))
print(x)
print(y)
print("-----------------------------------------------")
