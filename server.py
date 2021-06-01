from main.notifications.youtube import Youtube
from main.config import Config
from flask import Flask
from flask import request
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
  
app = Flask(__name__)
  
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

@app.route('/twitch_stream', methods = ['GET'])
def challenge_twitch():
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
  print(request.get_data())
  return "Received!"
  
if __name__ == "__main__":
  app.run(host="0.0.0.0")
