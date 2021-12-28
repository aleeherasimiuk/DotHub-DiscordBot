import requests
from ..webhook_message import WebhookMessage
from ..config import Config
import json


class TwitchNotification(WebhookMessage):
    user_name: str
    user_login: str
    stream_id: str

    def __init__(self, config: Config, user_name, user_login, role_id, stream_id):
        self.user_name = user_name
        self.user_login = user_login
        self.stream_id = stream_id

        content = f"¡Hey! ¡[{user_name}](https://twitch.tv/{user_login}) está en directo en <@&{role_id}>!"
        super().__init__(config, [], content=content)



class TwitchNotificationBuilder:

    user_name: str
    user_login: str
    stream_id: str

    def __init__(self, **kwargs):
        event = kwargs['event']
        self.user_login = event['broadcaster_user_login']
        self.user_name = event['broadcaster_user_name']
        self.stream_id = event['id']

    def _get_role_id(self):
        with open('res/roles.json') as f:
            _json = json.load(f)
        return _json['twitch_viewer']

    def build_twitch_notification(self, config: Config):
        role_id = self._get_role_id()
        return TwitchNotification(config, self.user_name, self.user_login, role_id, self.stream_id)
