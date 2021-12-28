from unittest import mock

import json
from models.config import Config
from models.notifications.twitch import TwitchNotification, TwitchNotificationBuilder
import unittest
from unittest.mock import Mock, MagicMock

@unittest.skip("Needs to refactor")
class TwitchNotificationTest(unittest.TestCase):

  twitch_notification_builder: TwitchNotificationBuilder
  mock_response = None

  def setUp(self):
    self.twitch_notification_builder = TwitchNotificationBuilder("user-id", "client-id", "auth-token")

  @mock.patch("requests.get")
  def test_mock_twitch_request(self, mock_get):
    response = self.mock_response(mock_get)
    self.assertEqual(response.status_code, 200)

  @mock.patch("requests.get")
  def test_mock_twitch_response(self, mock_get):
    response = self.mock_response(mock_get)
    self.assertEqual(response.json(), json.loads(self.expected_data()))

  @mock.patch("requests.get")
  def test_mock_twitch_channel_name(self, mock_get):
    response = self.mock_response(mock_get)
    self.twitch_notification_builder._process_request(response)
    self.assertEqual(self.twitch_notification_builder.user_name, "This is the User name")

  @mock.patch("requests.get")
  def test_mock_twitch_stream_title(self, mock_get):
    response = self.mock_response(mock_get)
    self.twitch_notification_builder._process_request(response)
    self.assertEqual(self.twitch_notification_builder.stream_title, "This is the stream title")

  @mock.patch("requests.get")
  def test_mock_twitch_user_login(self, mock_get):
    response = self.mock_response(mock_get)
    self.twitch_notification_builder._process_request(response)
    self.assertEqual(self.twitch_notification_builder.user_login, "userlogin")


  def mock_response(self, mock_get):
    expected = self.expected_data()
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = json.loads(expected)
    return self.twitch_notification_builder._make_request()

  def expected_data(self):
    return """\
      {
        "data": [
            {
                "id": "42151379981",
                "user_id": "199811071",
                "user_login": "userlogin",
                "user_name": "This is the User name",
                "game_id": "73586",
                "game_name": "This is de Game Name",
                "type": "live",
                "title": "This is the stream title",
                "viewer_count": 13478,
                "started_at": "2021-05-31T21:58:33Z",
                "language": "es",
                "thumbnail_url": "https://static-cdn.jtvnw.net/previews-ttv/live_user_asd-{width}x{height}.jpg",
                "tag_ids": [
                    "d4bb9c58-2141-4881-bcdc-3fe0505457d1"
                ],
                "is_mature": false
            }
        ],
        "pagination": {}
      }"""
