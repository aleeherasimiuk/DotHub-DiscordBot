
from models.logger import setup_discord_logger as setup_logger
import discord
from discord.ext import commands
import io, re, json
import textwrap
import traceback
import random
from contextlib import *
import datetime
import os

import json
import logging

description = 'N/A'
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.emojis = True
intents.messages = True
intents.reactions = True
intents.presences = True
bot = commands.Bot(command_prefix="$", description=description, intents=intents)
bot.remove_command('help')

logger = setup_logger("logs/dotesting.log")

with open("res/dotesting.json") as file:
    bot_config = json.load(file)

@bot.event
async def on_ready():
    logger.info(f"Bot started as {bot.user.name} [{bot.user.id}]")
    
@bot.command()
async def avatar(ctx, member : discord.Member = None):
    if member == None:
        await ctx.send(ctx.author.avatar_url)
    else:
        await ctx.send(member.avatar_url)
    
@bot.command()
async def scrap(ctx):
    if ctx.author.id not in bot_config['allowed_ids']:
        logger.warn(f"{ctx.author.id} attempted to scrap messages. Not allowed.")
        return
    messages = []
    logger.info("Scraping started")
    names = ["Juan", "José", "Adrian", "Mario", "Pedro", "Jacinto", "Antonio"]
    total_count = 1
    async for message in ctx.channel.history(limit=50000, oldest_first=True):
        if not message.content:
            continue
        text = discord.utils.remove_markdown(message.clean_content)
        s = re.split(r'<@!?(\d+)>', text)
        i = 0
        if (total_count % 100) == 0:
            logger.info(f"{total_count} messages have been downloaded.")
        for mention in s:
            try:
                mention = int(mention)
            except ValueError:
                continue
            if mention in message.raw_mentions:
                u = bot.get_user(mention)
                if not u:
                    random.seed(alguna_id)
                    name = random.choice(names)
                else:
                    name = u.name
                s[i].replace(mention, f"@{name}")
            i += 1
        text = "".join(s)
        s = re.split(r'<a?(:\w+:)(\d+)>', text)
        emojis = re.findall(r'<a?(:\w+:)(\d+)>', text)
        for emoji in emojis:
            if emoji[1] in s:
                s.remove(emoji[1])
        text = "".join(s)
        m = {"content": text, "author":f"{message.author.name}#{message.author.discriminator}", "created_at":message.created_at.isoformat()}
        messages.append(m)
        total_count += 1
    with open('results/scrapped.json', 'w', encoding="UTF-8") as f:
        json.dump(messages, f)   

@bot.command()
async def scrap_images(ctx):
    if ctx.author.id not in bot_config['allowed_ids']:
        logger.warn(f"{ctx.author.id} attempted to scrap images. Not allowed.")
        return
    await ctx.send("Iniciando scraping...")
    logger.info(f"Scraping images on: {ctx.channel.name}")
    messages = []
    total_count = 1
    start = datetime.datetime(year=2021, month=5, day=17, hour=21, minute=43)
    async for message in ctx.channel.history(limit=None, oldest_first=True, after=start):
        text = discord.utils.remove_markdown(message.clean_content)
        s = re.split(r'<@!?(\d+)>', text)
        i = 0
        if (total_count % 100) == 0:
            logger.info(f"{total_count} messages have been downloaded.")
        if message.attachments and message.attachments[0].content_type.startswith("image"):
            if message.content:
                text = message.content
            else:
                text = None
            m = {"title": text, "author":f"{message.author.name}#{message.author.discriminator}", "image_url":message.attachments[0].url, "original_message": message.junp_url}
            messages.append(m)
        total_count += 1
    with open('results/scrapped_images.json', 'w', encoding="UTF-8") as f:
        json.dump(messages, f)


@bot.command()
async def eval(ctx, *, body: str):
    if ctx.author.id not in bot_config['allowed_ids']:
        logger.warn(f"{ctx.author.id} attempted to eval an expression. Not allowed.")
        return
    
    if "sudo" in body:
        logger.warn(f"{ctx.author.id} attempted to eval an expression with sudo. Not allowed.")
        await ctx.send('👀')
        return

    """Evaluates a code"""
    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
    }
    env.update(globals())
    stdout = io.StringIO()
    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
    logger.info(f"Evaluating expression: {to_compile}")
    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction('\u2705')
        except:
            pass
        if ret is None:
            if value:
                await ctx.send(f'```py\n{value}\n```')
        else:
            await ctx.send(f'```py\n{value}\n```')



@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    if ctx.author.id not in bot_config['allowed_ids']:
        logger.warn(f"{ctx.author.id} attempted to ping. Not allowed.")
        return
    await ctx.send("Pong")

bot.run(os.environ['TOKEN'])
