import unittest
from main.config import Config


class ConfigTest(unittest.TestCase):

  def test_config_file_does_not_exist(self):
    with self.assertRaises(Exception):
      Config.from_file("this_file_does_not_exist")

  def test_error_on_config_key_typo(self):
    fake_json = {
      'username': 'username',
      'webhook_url': 'webhook_url',
      'avatar-url': 'avatar_url'
    }
    with self.assertRaises(Exception) as error:
      Config.from_json(fake_json)

  def test_error_on_config_key_key_invalid(self):
    fake_json = {
      'username': 'username',
      'webhook_url': 'webhook_url',
      'avatar_url': 'avatar_url',
      'fake_key': 'fake_key'
    }
    with self.assertRaises(Exception) as error:
      Config.from_json(fake_json)

  def test_error_on_config_key_key_missing(self):
    fake_json = {
      'username': 'username',
      'webhook_url': 'webhook_url',
    }
    with self.assertRaises(Exception) as error:
      Config.from_json(fake_json)

  def test_valid_config_username(self):
    valid_json = {
      'username': 'username',
      'webhook_url': 'https://discord.com/api/webhooks',
      'avatar_url': 'avatar_url'
    }
    config = Config.from_json(valid_json)
    self.assertEqual('username', config.username)

  def test_valid_config_webhook_url(self):
    valid_json = {
      'username': 'username',
      'webhook_url': 'https://discord.com/api/webhooks',
      'avatar_url': 'avatar_url'
    }
    config = Config.from_json(valid_json)
    self.assertEqual('https://discord.com/api/webhooks', config.webhook_url)

  def test_valid_config_avatar(self):
    valid_json = {
      'username': 'username',
      'webhook_url': 'https://discord.com/api/webhooks',
      'avatar_url': 'avatar_url'
    }
    config = Config.from_json(valid_json)
    self.assertEqual('avatar_url', config.avatar_url)

  def test_invalid_config_webhook_url(self):
    valid_json = {
      'username': 'username',
      'webhook_url': 'https://google.com',
      'avatar_url': 'avatar_url'
    }
    with self.assertRaises(Exception):
      Config.from_json(valid_json)
