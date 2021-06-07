from main.notifications.twitch import TwitchNotification, TwitchNotificationBuilder
from main.notifications.youtube import YoutubeNotification
from main.config import Config
from flask import Flask, config
from flask import request
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json
import logging
import requests

app = Flask(__name__)
LOG_FILENAME = 'logs/errores.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


@app.route('/youtube_video', methods=['POST'])
def receive_youtube_notification():
    app.logger.info("Received youtube notification.")

    config = Config.from_file('res/notifications_config.json')
    youtube_message = YoutubeNotification.from_xml(config, request.get_data())

    app.logger.info("Sending webhook message for: {} - {}".format(youtube_message.channel_name, youtube_message.title))
    youtube_message.send()
    return "", 204


@app.route('/youtube_video', methods=['GET'])
def challenge():
    challenge = request.args.get('hub.challenge')
    app.logger.info("Challenge for youtube subscription received: {}".format(challenge))

    if challenge:
        return challenge

    return '', 204


@app.route("/")
def hello():
    return "Hola Dothub!"


@app.route('/twitch_stream', methods=['POST'])
def receive_twitch_notification():
    _json = json.loads(request.get_data())

    if 'challenge' in _json.keys():
        challenge = _json['challenge']
        app.logger.info("Challenge for youtube subscription received: {}".format(challenge))
        return challenge

    file = open('res/twitch_config.json')
    _json = json.load(file)
    file.close()

    try:
        config = Config.from_file('res/notifications_config.json')
        twitch_notification = TwitchNotificationBuilder(**_json).build_twitch_notification(config)
        twitch_notification.send()
    except Exception as e:
        app.logger.error("Can't send twitch notification: {}".format(e))

    app.logger.info(
        "Sending webhook message for: {} - {}".format(twitch_notification.user_name, twitch_notification.stream_title))

    return '', 204


@app.route('/twitch_stream_test', methods=['POST'])
def receive_twitch_notification_test():
    _json = json.loads(request.get_data())

    data = _json['data'][0]
    user_name = data['user_name']
    user_login = data['user_login']
    title = data['title']
    app.logger.info("Received test twitch notification: {} - {}".format(user_name, title))

    config = Config.from_file('res/notifications_config.json')
    twitch_notification = Twitch(config, user_name, user_login, title)
    twitch_notification.send()

    return '', 204


@app.route('/logs')
def logs():
    file = open(LOG_FILENAME, "r")
    return file.read()

@app.route('/dotesting')
def dotesting_logs():
    file = open("logs/dotesting.log", "r")
    return "<br>".join(file.read().splitlines())


if __name__ == "__main__":
    app.run(host="0.0.0.0")
