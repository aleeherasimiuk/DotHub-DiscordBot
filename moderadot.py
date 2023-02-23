import discord
from discord.ext import commands
from models.embed.ban import Ban
import json
from models.logger import setup_discord_logger as setup_logger
import os

CONFIG_FILE = "res/moderadot.json"

logger = setup_logger("logs/moderadot.log")

bot_config = None
with open(CONFIG_FILE) as file:
    bot_config = json.load(file)

message_content = ""
last_message = ""
last_message_content = ""
spam_counter = 0

description = 'N/A'
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.emojis = True
intents.messages = True
intents.reactions = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix = ">", description = description, intents = intents)
bot.remove_command('help')

@bot.event
async def on_message(message):
    global last_message, last_message_content, spam_counter
    message_content = f"{message.author.id}: {message.content}"
    message_content = message_content.replace("'", "<c>")
    if message_content == last_message_content and message.content != "":
        spam_counter += 1
        await message.delete()
        logger.warning(f"User Spam: {message_content}")
    else:
        last_message_content = message_content
        spam_counter = 0
    if spam_counter > 2:
        await last_message.delete()
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

@bot.command()
async def ping(ctx):
    if ctx.author.id not in bot_config['allowed_ids']:
        logger.warn(f"{ctx.author.id} attempted to ping. Not allowed.")
        return
    await ctx.send("Pong")


bot.run(os.environ['TOKEN'])
