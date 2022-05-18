import discord
import os
from discord.ext import commands
from models.metadata.stegano import get_metadata_from_steno
from models.metadata.xmp import get_metadata_from_xmp
from models.artwork import Artwork
from models.logger import setup_discord_logger as setup_logger
import aiohttp

description = 'N/A'
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.emojis = True
intents.messages = True
intents.reactions = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix=".", description=description, intents=intents)
bot.remove_command('help')

TOKEN = os.environ['TOKEN']
IMAGES_CHANNEL = os.environ['IMAGES_CHANNEL']
MUSEUM_CHANNEL = os.environ['MUSEUM_CHANNEL']
ALLOWED_ADMIN = [285598698593845249, 239203656405221376, 451817627808169985, 524301093014994956]
EMOJI = "🖼️"
CANCEL_EMOJI = "❌"
ALREADY_PUBLISHED_EMOJI = "✅"
THRESHOLD = 1

logger = setup_logger("logs/museum.log")

@bot.event
async def on_ready():
    logger.info(f"Bot started as {bot.user.name} [{bot.user.id}]")
    logger.info("{} {} {}".format(TOKEN, IMAGES_CHANNEL, MUSEUM_CHANNEL))
    await bot.change_presence(activity = discord.Game(name = "/museo"))



@bot.event
async def on_raw_reaction_add(payload):
    channel_id = str(payload.channel_id)
    emoji = str(payload.emoji)

    if channel_id != IMAGES_CHANNEL:
        return

    if str(payload.emoji) != EMOJI:
        return

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if not message.attachments or not message.attachments[0].content_type.startswith("image"):
        return

    emojis_in_this_message = {r.emoji: (r.count, r.users().map(lambda user: user.id)) for r in message.reactions}

    count, users = emojis_in_this_message.get(CANCEL_EMOJI, (0, []))
    if count and await users.find(lambda user: user in ALLOWED_ADMIN):
        return

    count, users = emojis_in_this_message.get(ALREADY_PUBLISHED_EMOJI, (0, []))
    if count and await users.find(lambda user: user == bot.user.id):
        return

    count, _ = emojis_in_this_message[EMOJI]
    if count < THRESHOLD:
        return

    metadata = await extract_metadata(message)
    museum = bot.get_channel(int(MUSEUM_CHANNEL))
    if metadata:
        title = metadata["title"]
    else:
        title = message.content or "Sin título"

    artwork = Artwork(title, message.jump_url, message.attachments[0].url, message.author.display_name)
    embed = artwork.discord_embed()
    museum = bot.get_channel(int(MUSEUM_CHANNEL))
    await museum.send(embed=embed)
    await message.add_reaction(ALREADY_PUBLISHED_EMOJI)

    
@bot.command()
async def ping(ctx):
    if ctx.author.id not in ALLOWED_ADMIN:
        logger.warn(f"{ctx.author.id} attempted to ping. Not allowed.")
        return
    await ctx.send("Pong")

@bot.command()
async def change_threshold(ctx, *, body):
    if ctx.author.id not in ALLOWED_ADMIN:
        logger.warn(f"{ctx.author.id} attempted to change threshold. Not allowed.")
        await ctx.send("Solo administradores pueden cambiar el THRESHOLD")
        return
    global THRESHOLD
    try:
      THRESHOLD = int(body)
      await ctx.send(f"Threshold changed to {THRESHOLD}")
    except ValueError:
      await ctx.send(f"El threshold debe ser un número")
      
    

@bot.slash_command(name = "museo", description = "Obtener información acerca del museo")
async def museo(ctx):
    await ctx.respond(f"La obra se publicará en el museo cuando obtenga {THRESHOLD} reacciones de {EMOJI}\nSi la la obra contiene una {CANCEL_EMOJI} de un admin la publicación no se subirá al museo.\nSi la obra ya tiene {ALREADY_PUBLISHED_EMOJI} ya se publicó en el museo.")


async def extract_metadata(message):

    stream = await get_stream(message)

    metadata = get_metadata_from_xmp(stream)

    if not metadata:
        metadata = get_metadata_from_steno(stream)

    if not metadata:
        return None

    size = get_size(message)
    metadata.update(author_id = message.author.id, thumbnail_url = message.attachments[0].url, size = size)
    return metadata


async def get_stream(message):
    async with aiohttp.ClientSession() as session:
        async with session.get(message.attachments[0].url) as resp:
            stream = await resp.read()
    return stream


def get_size(message):
    return f"{message.attachments[0].width} x {message.attachments[0].height}"


bot.run(TOKEN)