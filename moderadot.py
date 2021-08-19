import discord
from discord.ext import commands
from main.embed.ban import Ban
import json
from main.logger import setup_logger
import logging

CONFIG_FILE = "res/moderadot.json"
LOG_FILE = "logs/moderadot.log"

logger = setup_logger(logging.getLogger('discord'), LOG_FILE, logging.INFO)

bot_config = None
with open(CONFIG_FILE) as file:
    bot_config = json.load(file)

message_content = ""
last_message = ""
spam_counter = 0

bot = commands.Bot(command_prefix='>')

@bot.event
async def on_message(message):
    global message_content, last_message, spam_counter
    message_content = f"{message.author.id}: {message.content}"
    message_content = message_content.replace("'", "<c>")
    if message_content == last_message and message.content != "":
        spam_counter += 1
        await message.delete()
        logger.warning(f"User Spam: {message_content}")
    else:
        last_message = message_content
        spam_counter = 0
    if spam_counter > 2:
        user = message.author
        muted = discord.utils.get(user.guild.roles, name="muted")
        verified = discord.utils.get(user.guild.roles, name="Member")
        await user.add_roles(muted)
        await user.remove_roles(verified)
        logger.info(f"Muted User: {message_content}")
        channel_log = await bot.fetch_channel(bot_config['channel_log'])
        banMessage = Ban(user, message.content)
        await channel_log.send(embed=banMessage.discord_embed())
    await bot.process_commands(message)

@bot.event
async def on_ready():
    logger.info(f"Bot started as {bot.user.name} [{bot.user.id}]")
    await bot.change_presence(activity = discord.Game(name = "Observando el ServiDot"))


bot.run(bot_config['token'])
