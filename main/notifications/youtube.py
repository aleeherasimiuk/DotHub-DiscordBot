from bs4 import BeautifulSoup
from ..webhook_message import WebhookMessage
from ..config import Config


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

        content = "Hey @everyone! [{}](<{}>) ha subido un nuevo [vídeo]({})!".format(channel_name, channel_url, video_url)
        super().__init__(config, [], content=content)

    @classmethod
    def from_xml(cls, config: Config, _xml):
        soup = BeautifulSoup(_xml, 'lxml')
        title = soup.entry.title.string
        video_url = soup.entry.link.get('href')
        channel_url = soup.entry.author.uri.string
        channel_name = soup.entry.author.find('name').string

        return YoutubeNotification(config, channel_name, channel_url, title, video_url)
