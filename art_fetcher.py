import os
from main.fetching_config import FetchingConfig
import sys
import discord
import logging
import json
from discord import member

from discord.utils import find

from main.artwork import Artwork
from main.webhook_message import WebhookMessage
from main.config import Config

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='a')
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

class MyClient(discord.Client):
    artworks = []
    emoji = '🎨'
    config: FetchingConfig
    last_message: None

    def __init__(self):
        self.config = FetchingConfig.from_file('res/bot.json')
        super().__init__()

    async def on_ready(self):
        logger.info('Logged on as {0}!'.format(self.user))
        messages_with_image = await self.fetch_messages_with_image()
        raw_artworks = messages_with_image.filter(self.is_artwork)
        _processed_artworks = raw_artworks.map(self.process_artwork)
        self.artworks = await _processed_artworks.map(lambda x: x.to_dict()).flatten()
        

        if not self.last_message:
            logger.info("No artworks were retrieved")
            return
         
        logger.info("Fetching ended. Saving file.")
        self.save_file()

        next_starting_point = self.last_message.id
        logger.info(f"Next starting point: {next_starting_point}")
        self.config.change_starting_point(next_starting_point, 'res/bot.json')
        self.last_message = None
        logger.info("Finished")

    def save_file(self):
        old_pending_artworks = []
        if os.path.getsize(self.config.save_path):
            with open(self.config.save_path, 'r') as f:
                old_pending_artworks = json.load(f)

        with open(self.config.save_path, 'w') as f:
            old_pending_artworks.extend(self.artworks)
            json.dump(old_pending_artworks, f)
        self.artworks = []

    async def is_artwork(self, message):
        reaction_with_art_icon = find(lambda reaction: reaction.emoji == self.emoji, message.reactions)
        if not reaction_with_art_icon:
            return False

        users_reacted = reaction_with_art_icon.users()
        return await users_reacted.find(self.is_allowed_reactor)

    def is_allowed_reactor(self, user):
        return f"{user.name}#{user.discriminator}" in self.config.allowed_reactors

    async def fetch_messages_with_image(self):
        channel = await self.fetch_channel(self.config.channel_id)
        logger.info(f'Scanning channel: #{channel}')
        starting_point = await channel.fetch_message(self.config.starting_point)
        return channel.history(after=starting_point).filter(lambda message: message.attachments)

    async def process_artwork(self, message):
        await message.clear_reaction(emoji = self.emoji)
        await message.add_reaction(emoji = self.emoji)

        _artwork = Artwork.from_discord_message(message)
        logger.info(f"Fetching: {_artwork.title}")
        self.last_message = message
        return _artwork

    async def on_message(self, message):
        pass


client = MyClient()
client.run(client.config.token)
