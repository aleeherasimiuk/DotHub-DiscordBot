from main.config import Config
from main.notifications.youtube import YoutubeNotification
import unittest

class YoutubeNotificationTest(unittest.TestCase):
  
  youtube_notification : YoutubeNotification

  def setUp(self):
    config = Config("https://discord.com/api/webhooks/0/0", "https://google.com/image.jpg", "TestUsername")
    self.youtube_notification = YoutubeNotification.from_xml(config, self.xml)

  def test_channel_name(self):
    self.assertEqual(self.youtube_notification.channel_name, "Channel Name")

  def test_video_title(self):
    self.assertEqual(self.youtube_notification.title, "This is the video title!")

  def test_video_url(self):
    self.assertEqual(self.youtube_notification.video_url, "https://www.youtube.com/watch?v=123456789")

  def test_channel_url(self):
    self.assertEqual(self.youtube_notification.channel_url, "https://www.youtube.com/channel_name")

  xml = """<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015"
         xmlns="http://www.w3.org/2005/Atom">
  <link rel="hub" href="https://pubsubhubbub.appspot.com"/>
  <link rel="self" href="https://www.youtube.com/xml/feeds/videos.xml?channel_id=CHANNEL_ID"/>
  <title>YouTube video feed</title>
  <updated>2015-04-01T19:05:24.552394234+00:00</updated>
  <entry>
    <id>1234567489</id>
    <yt:videoId>123456789</yt:videoId>
    <yt:channelId>this_is_the_channel_id</yt:channelId>
    <title>This is the video title!</title>
    <link rel="alternate" href="https://www.youtube.com/watch?v=123456789"/>
    <author>
     <name>Channel Name</name>
     <uri>https://www.youtube.com/channel_name</uri>
    </author>
    <published>2015-03-06T21:40:57+00:00</published>
    <updated>2015-03-09T19:05:24.552394234+00:00</updated>
  </entry>
</feed>"""