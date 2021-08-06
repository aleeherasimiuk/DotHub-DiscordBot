import discord
from discord.ext import commands
from os import system
from datetime import datetime
import json

CONFIG_FILE = "res/moderadot.json"

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
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message_content = f"{message.author.id}: {message.content}"
    message_content = message_content.replace("'", "<c>")
    if message_content == last_message:
        spam_counter += 1
        await message.delete()
        system(f"echo '{date} {message_content}' >> muted.log")
    else:
        last_message = message_content
        spam_counter = 0
        system(f"echo '{date} {message_content}' >> all.log")
    if spam_counter > 1:
        user = message.author
        muted = discord.utils.get(user.guild.roles, name="muted")
        verified = discord.utils.get(user.guild.roles, name="Member")
        await user.add_roles(muted)
        await user.remove_roles(verified)
        system(f"echo 'Muted User: {date} {message_content}' >> muted.log")
    await bot.process_commands(message)
bot.run(bot_config['token'])
