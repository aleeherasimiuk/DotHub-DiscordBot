import requests
from ..webhook_message import WebhookMessage
from ..config import Config
import json


class TwitchNotification(WebhookMessage):
    user_name: str
    user_login: str
    stream_title: str

    def __init__(self, config: Config, user_name, user_login, title, role_id):
        self.user_name = user_name
        self.user_login = user_login
        self.stream_title = title

        content = f"¡Hey! [{user_name}](https://twitch.tv/{user_login}) está en directo en <@&{role_id}>: **{title}**.\n¡No te lo pierdas!"
        super().__init__(config, [], content=content)


class TwitchNotificationBuilder:
    _user_id: str
    _client_id: str
    _auth_token: str

    user_name: str
    user_login: str
    stream_title: str

    def __init__(self, user_id, client_id, auth_token):
        self._user_id = user_id
        self._client_id = client_id
        self._auth_token = auth_token

    def _make_request(self):
        return requests.get("https://api.twitch.tv/helix/streams?user_id={}".format(self._user_id),
                            headers={'client-id': self._client_id, 'authorization': self._auth_token})

    def _process_request(self, response):
        self._validate_response(response)
        self._get_data_from_response(response)

    def _get_data_from_response(self, response):
        json_response = response.json()['data']

        if not json_response:
            raise Exception("There was an error retrieving info from stream: Empty data")

        data = json_response[0]
        self.user_name = data['user_name']
        self.user_login = data['user_login']
        self.stream_title = data['title']

    def _validate_response(self, response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise Exception("There was an error retrieving info from stream")

    def _get_role_id(self):
        with open('res/roles.json') as f:
            _json = json.load(f)
        return _json['twitch_viewer']

    def build_twitch_notification(self, config: Config):
        response = self._make_request()
        self._process_request(response)
        role_id = self._get_role_id()
        return TwitchNotification(config, self.user_name, self.user_login, self.stream_title, role_id)
