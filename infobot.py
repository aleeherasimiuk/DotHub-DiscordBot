import discord
import logging
import json
import aiohttp
from discord.ext import commands
from main.metadata.stegano import get_metadata_from_steno
from main.metadata.xmp import get_metadata_from_xmp
from main.embed.info import Info
from main.logger import setup_logger

description = 'N/A'
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.emojis = True
intents.messages = True
intents.reactions = True
intents.presences = True
bot = commands.Bot(command_prefix = "&", description = description, intents = intents)
bot.remove_command('help')

CONFIG_FILE = "res/infobot.json"
LOG_FILE = "logs/infobot.log"
NOT_FOUND_MESSAGE = "No he podido obtener información acerca de esa imagen. 😔"

logger = setup_logger(logging.getLogger('discord'), LOG_FILE, logging.INFO)

bot_config = None
with open(CONFIG_FILE) as file:
    bot_config = json.load(file)


@bot.event
async def on_message(message):
    if message.content.lower() == "info" and message.reference:
        await extract_metadata(message)
    await bot.process_commands(message)


async def extract_metadata(message):
    reference = await message.channel.fetch_message(message.reference.message_id)

    if not reference.attachments or not reference.attachments[0].content_type.startswith("image"):
        return

    stream = await get_stream(reference)

    metadata = get_metadata_from_xmp(stream)

    if not metadata:
        metadata = get_metadata_from_steno(stream)

    if not metadata:
        await send_message(message, discord.Embed(description = NOT_FOUND_MESSAGE, color = 16122))
        return

    size = get_size(reference)
    metadata.update(author_id = reference.author.id, thumbnail_url = reference.attachments[0].url, size = size)
    info = Info(**metadata)
    await send_message(message, info.discord_embed())


async def get_stream(reference):
    async with aiohttp.ClientSession() as session:
        async with session.get(reference.attachments[0].url) as resp:
            stream = await resp.read()
    return stream


def get_size(reference):
    return f"{reference.attachments[0].width} x {reference.attachments[0].height}"


async def send_message(message, payload):
    await message.channel.send(embed = payload, reference = message, mention_author=False)


@bot.command()
async def ping(ctx):
    if ctx.author.id not in bot_config['allowed_ids']:
        logger.warn(f"{ctx.author.id} attempted to ping. Not allowed.")
        return
    await ctx.send("Pong")

@bot.event
async def on_ready():
    logger.info(f"Bot started as {bot.user.name} [{bot.user.id}]")
    await bot.change_presence(activity = discord.Game(name = "VQGAN + CLIP"))

bot.run(bot_config['token'])
