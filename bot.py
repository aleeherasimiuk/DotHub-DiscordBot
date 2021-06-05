import discord
import asyncio
from discord.ext import commands
import io, re, json
import textwrap
import traceback
import contextlib
import random
from contextlib import *
import datetime
import xmltodict, json
import aiohttp

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

@bot.event
async def on_ready():
    print('Conectado como:')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
@bot.command()
async def avatar(ctx, member : discord.Member = None):
    """Esta es la descripción del comando"""
    if member == None:
        await ctx.send(ctx.author.avatar_url)
    else:
        await ctx.send(member.avatar_url)
    

@bot.command()
async def scrap(ctx):
    if ctx.author.id != 239203656405221376:
        return
    messages = []
    print("Started")
    names = ["Juan", "José", "Adrian", "Mario", "Pedro", "Jacinto", "Antonio"]
    total_count = 1
    async for message in ctx.channel.history(limit=50000, oldest_first=True):
        if not message.content:
            continue
        text = discord.utils.remove_markdown(message.clean_content)
        s = re.split(r'<@!?(\d+)>', text)
        i = 0
        if (total_count % 100) == 0:
            print(f"{total_count} mensajes han sido descargados.")
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
    with open('mensajes.json', 'w', encoding="UTF-8") as f:
        json.dump(messages, f)   

@bot.command()
async def scrap_images(ctx):
    if ctx.author.id != 239203656405221376:
        return
    await ctx.send("Iniciando scraping...")
    messages = []
    total_count = 1
    start = datetime.datetime(year=2021, month=5, day=17, hour=21, minute=43)
    async for message in ctx.channel.history(limit=None, oldest_first=True, after=start):
        text = discord.utils.remove_markdown(message.clean_content)
        s = re.split(r'<@!?(\d+)>', text)
        i = 0
        if (total_count % 100) == 0:
            print(f"{total_count} mensajes han sido descargados.")
        if message.attachments and message.attachments[0].content_type.startswith("image"):
            if message.content:
                text = message.content
            else:
                text = None
            m = {"content": text, "author":f"{message.author.name}#{message.author.discriminator}", "url":message.attachments[0].url}
            messages.append(m)
        total_count += 1
    with open('imagenes.json', 'w', encoding="UTF-8") as f:
        json.dump(messages, f)






@bot.command()
async def eval(ctx, *, body: str):
    if ctx.author.id != 239203656405221376:
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
    if message.content.lower() == "info" and message.reference:
        msg = await message.channel.fetch_message(message.reference.message_id)
        if not msg.attachments or not msg.attachments[0].content_type.startswith("image"):
            pass
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(msg.attachments[0].url) as resp:
                    d = await resp.read()
            xmp_start = d.find(b'<x:xmpmeta')
            xmp_end = d.find(b'</x:xmpmeta')
            xmp_str = d[xmp_start:xmp_end+12]
            if not xmp_str:
                await message.channel.send("Esta imagen no contiene metadatos en XMP.", reference=msg)
                return
            o = xmltodict.parse(xmp_str)
            meta_string = json.dumps(o)
            meta = json.loads(meta_string)
            meta = meta["x:xmpmeta"]["rdf:RDF"]["rdf:Description"]
            notebook = meta["dc:creator"]["rdf:Seq"]["rdf:li"]
            title = meta["dc:title"]["rdf:Seq"]["rdf:li"]
            model = meta["dc:model"]["rdf:Seq"]["rdf:li"]
            i = meta["dc:i"]["rdf:Seq"]["rdf:li"]
            seed = meta["dc:seed"]["rdf:Seq"]["rdf:li"]
            await message.channel.send(f"**Notebook:** {notebook}\n**Título(s):** {title}\n**Modelo:** {model}\n**Iteraciones:** {i}\n**Seed:** {seed}", reference=msg)
    await bot.process_commands(message)
            
   
bot.run('token_del_bot')
