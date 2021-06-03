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

    def __init__(self):
        self.config = FetchingConfig.from_file('res/bot.json')
        super().__init__()

    async def on_ready(self):
        logger.info('Logged on as {0}!'.format(self.user))
        messages_with_image = await self.fetch_messages_with_image()

        last_message = None
        async for message in messages_with_image:

            if not await self.is_artwork(message): 
                continue
            
            await message.clear_reaction(emoji = self.emoji)
            await message.add_reaction(emoji = self.emoji)

            artwork = Artwork.from_discord_message(message)
            logger.info(f"Fetching: {artwork.title}")

            artwork_json = artwork.to_dict()
            self.artworks.append(artwork_json)
            last_message = message

        
        if not last_message:
            logger.info("No artworks were retrieved")
            return
         
        logger.info("Fetching ended. Saving file.")
        self.save_file()

        next_starting_point = last_message.id()
        logger.info(f"Next starting point: {id}")
        self.config.change_starting_point(next_starting_point, 'res/bot.json')
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

    async def on_message(self, message):
        pass


client = MyClient()
client.run(client.config.token)
