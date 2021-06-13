from bs4 import BeautifulSoup
from ..webhook_message import WebhookMessage
from ..config import Config
import json


class YoutubeNotification(WebhookMessage):
    channel_name: str
    channel_url: str
    title: str
    video_url: str

    def __init__(self, config: Config, channel_name, channel_url, title, video_url):
        self.channel_name = channel_name
        self.channel_url = channel_url
        self.title = title
        self.video_url = video_url
        role_id = self._get_role_id()

        content = f"¡Hey! ¡[{channel_name}](<{channel_url}>) ha subido un nuevo [vídeo]({video_url}) en <@&{role_id}>!"
        super().__init__(config, [], content=content)

    @classmethod
    def from_xml(cls, config: Config, _xml):
        soup = BeautifulSoup(_xml, 'lxml')
        title = soup.entry.title.string
        video_url = soup.entry.link.get('href')
        channel_url = soup.entry.author.uri.string
        channel_name = soup.entry.author.find('name').string

        return YoutubeNotification(config, channel_name, channel_url, title, video_url)

    def _get_role_id(self):
        with open('res/roles.json') as f:
            _json = json.load(f)
        return _json['youtube_viewer']
