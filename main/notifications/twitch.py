import requests
from ..webhook_message import WebhookMessage
from ..config import Config


class TwitchNotification(WebhookMessage):
    user_name: str
    user_login: str
    stream_title: str

    def __init__(self, config: Config, user_name, user_login, title):
        self.user_name = user_name
        self.user_login = user_login
        self.stream_title = title

        content = "Hey @everyone! [{}](https://twitch.tv/{}) está en directo en Twitch: **{}**.\nNo te lo pierdas!".format(
            user_name, user_login, title)
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

    def build_twitch_notification(self, config: Config):
        response = self._make_request()
        self._process_request(response)
        return TwitchNotification(config, self.user_name, self.user_login, self.stream_title)
