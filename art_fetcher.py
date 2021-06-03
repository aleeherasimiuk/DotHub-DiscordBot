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
    filename='discord.log', encoding='utf-8', mode='w')
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

file = open('res/bot.json', 'r')
_json = json.load(file)
file.close()


class MyClient(discord.Client):
    artworks = []
    emoji = '🎨'

    async def on_ready(self):
        logger.info('Logged on as {0}!'.format(self.user))
        messages_with_image = await self.fetch_messages_with_image()

        async for message in messages_with_image:

            if await self.is_artwork(message):
                await message.clear_reaction(emoji=self.emoji)
                await message.add_reaction(emoji=self.emoji)

            artwork = Artwork.from_discord_message(message)
            logger.info(f"Fetching: {artwork.title}")

            artwork_json = artwork.to_dict()
            self.artworks.append(artwork_json)

        logger.info("Fetching ended. Saving file.")
        with open('res/pending_artworks.json', 'w') as f:
            json.dump(self.artworks, f)

        logger.info("Finished")

    async def is_artwork(self, message):
        reaction_with_art_icon = find(
            lambda x: x.emoji == self.emoji, message.reactions)
        if not reaction_with_art_icon:
            return False

        users_reacted = reaction_with_art_icon.users()
        return await users_reacted.find(self.is_allowed_reactor)

    def is_allowed_reactor(self, user):
        return f"{user.name}#{user.discriminator}" in _json['allowed_reactors']

    async def fetch_messages_with_image(self):
        channel = await self.fetch_channel(_json['channel_id'])
        logger.info(f'Scanning channel: #{channel}')
        starting_point = await channel.fetch_message(_json['starting_point'])
        return channel.history(after=starting_point).filter(lambda x: x.attachments)

    async def on_message(self, message):
        pass


client = MyClient()
client.run(_json['token'])
