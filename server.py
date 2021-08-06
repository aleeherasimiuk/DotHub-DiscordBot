from main.notifications.twitch import TwitchNotificationBuilder
from main.notifications.youtube import YoutubeNotification
from main.config import Config
from main.logger import setup_logger
from flask import Flask
from flask import request
from flask import render_template
import json
import logging
import traceback

app = Flask(__name__)
SERVER_LOG_FILENAME = 'logs/errores.log'
DOTESTING_LOG_FILENAME = "logs/dotesting.log"
INFOBOT_LOG_FILENAME = "logs/infobot.log"
MODERADOT_LOG_FILENAME = "logs/moderadot.log"

logger = setup_logger(app.logger, SERVER_LOG_FILENAME, logging.INFO)

last_sent_youtube_notification = ""
last_sent_twitch_notification = ""


@app.route('/youtube_video', methods=['POST'])
def receive_youtube_notification():
    global last_sent_youtube_notification
    logger.info("Received youtube notification.")
    logger.debug("Received youtube payload: {}".format(request.get_data()))

    config = Config.from_file('res/mock_notifications_config.json')
    youtube_message = YoutubeNotification.from_xml(config, request.get_data())

    if youtube_message.title != last_sent_youtube_notification:
        logger.info("Sending webhook message for: {} - {}".format(youtube_message.channel_name, youtube_message.title))
        youtube_message.send()
        last_sent_youtube_notification = youtube_message.title
    
    return "", 204


@app.route('/youtube_video', methods=['GET'])
def challenge():
    challenge = request.args.get('hub.challenge')
    logger.info("Challenge for youtube subscription received: {}".format(challenge))

    if challenge:
        return challenge

    return '', 204


@app.route("/")
def hello():
    return "Hola Dothub!"


@app.route('/twitch_stream', methods=['POST'])
def receive_twitch_notification():
    global last_sent_twitch_notification
    _json = json.loads(request.get_data())
    logger.debug("Received twitch payload: {}".format(request.get_data()))

    if 'challenge' in _json.keys():
        challenge = _json['challenge']
        logger.info("Challenge for youtube subscription received: {}".format(challenge))
        return challenge

    try:
        config = Config.from_file('res/notifications_config.json')
        twitch_notification = TwitchNotificationBuilder(**_json).build_twitch_notification(config)
        if twitch_notification.stream_id not in last_sent_twitch_notification:
            twitch_notification.send()
            last_sent_twitch_notification = twitch_notification.stream_id
            logger.info("Sending webhook message for: {}".format(twitch_notification.user_name))
        else:
            logger.info("Duplicated twitch notification")
    except Exception as e:
        logger.error("Can't send twitch notification: {}".format(e))
        traceback.print_exc()

    
    return '', 204


@app.route('/logs')
def logs():
    return show_logs(SERVER_LOG_FILENAME)

@app.route('/dotesting')
def dotesting_logs():
    return show_logs(DOTESTING_LOG_FILENAME)

@app.route('/infobot')
def infobot_logs():
    return show_logs(INFOBOT_LOG_FILENAME)

@app.route('/moderadot')
def infobot_logs():
    return show_logs(MODERADOT_LOG_FILENAME)

def show_logs(filename):
    with open(filename, "r") as file:
        lines = file.read().splitlines()
    return render_template('logs.html', lines=lines)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
