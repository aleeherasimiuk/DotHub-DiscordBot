from main.notifications.twitch import Twitch
from main.notifications.youtube import Youtube
from main.config import Config
from flask import Flask, config
from flask import request
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json
import logging
import requests
  
app = Flask(__name__)
LOG_FILENAME = './errores.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
  
@app.route('/youtube_video', methods = ['POST'])
def receive_youtube_notification():
  soup = BeautifulSoup(request.get_data(), 'lxml')
  title = soup.entry.title.string 
  video_url = soup.entry.link.get('href')
  channel_url = soup.entry.author.uri.string
  channel_name = soup.entry.author.find('name').string

  config = Config.from_file('res/notifications_config.json')
  youtube_message = Youtube(config, channel_name, channel_url, title, video_url)
  youtube_message.send()    
  return "Received: {}".format(soup)

@app.route('/youtube_video', methods = ['GET'])
def challenge():
  challenge = request.args.get('hub.challenge')

  if challenge:
    return challenge
  
  print(request.data)

  return '', 204


@app.route("/")
def hello():
  return "Hola Dothub!"

@app.route('/twitch_stream', methods = ['POST'])
def receive_twitch_notification():
  _json = json.loads(request.get_data())

  if 'challenge' in _json.keys():
    return _json['challenge']

  file  = open('res/twitch_config.json')
  _json = json.load(file) 
  user_id = _json['user_id']
  client_id = _json['client_id']
  auth_token = _json['auth_token']
  file.close()

  response = requests.get("https://api.twitch.tv/helix/streams?user_id={}".format(user_id), headers={'client-id': client_id, 'authorization':auth_token})

  try:
    response.raise_for_status()
  except requests.exceptions.HTTPError as err:
    app.logger.error("There was an error retrieving stream name from twitch: {}".format(err))


  data = response.json()['data'][0]
  user_name = data['user_name']
  user_login = data['user_login']
  title = data['title']

  config = Config.from_file('res/notifications_config.json')
  twitch_notification = Twitch(config, user_name, user_login, title)
  twitch_notification.send()
  
  return '', 204
  
if __name__ == "__main__":
  app.run(host="0.0.0.0")
