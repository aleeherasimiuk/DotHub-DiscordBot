import discord
from discord.ext import commands
from os import system
from datetime import datetime

mensaje = ""
lmensaje = ""
n = 0

bot = commands.Bot(command_prefix='>')
@bot.listen()
async def on_message(message):
    global mensaje, lmensaje, n
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mensaje = f"{message.author.id}: {message.content}"
    mensaje = mensaje.replace("'", "<c>")
    if mensaje == lmensaje:
        n = n+1
        await message.delete()
        system(f"echo '{date} {mensaje}' >> muted.log")
    else:
        lmensaje = mensaje
        n = 0
        system(f"echo '{date} {mensaje}' >> all.log")
    if n > 1:
        user = message.author
        muted = discord.utils.get(user.guild.roles, name="muted")
        verified = discord.utils.get(user.guild.roles, name="Member")
        await user.add_roles(muted)
        await user.remove_roles(verified)
        system(f"echo 'USUARIO MUTEADO: {date} {mensaje}' >> muted.log")
    await bot.process_commands(message)
bot.run('')
