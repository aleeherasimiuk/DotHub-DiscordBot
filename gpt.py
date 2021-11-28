import discord
from discord.ext import commands
import aiohttp

#bot = .Bot()
intents = discord.Intents.default()
#intents.members = True
intents.guilds = True
intents.emojis = True
intents.messages = True
intents.reactions = True
intents.presences = True


bot = commands.Bot(command_prefix='=', intents=intents)
bot.remove_command('help')

@bot.slash_command(name = "gpt")
async def gpt(ctx, prompt: str):
    print("Using slash command")
    await ctx.defer()

    new_prompt = "BOT: ¡Buen Día!. Me llamo GPT-j y soy un bot que pertenece al Servidor de Discord de DotCSV. Puede hacerme la pregunta que quieras, o simplemente puedes charlar conmigo"
    new_prompt += "\nYO:" + prompt
    new_prompt += "\nBOT:"


    payload = {
        "context": new_prompt,
        "token_max_length": 128,
        "temperature": 1.0,
        "top_p": 0.9,
        "stop_sequence": "\n"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("http://api.vicgalle.net:5000/generate", params=payload) as response:
                json_response = await response.json()
                await ctx.respond(f"**Input:**\n```{prompt}```\n**Output:**\n```{json_response['text'].strip()}```")
    except Exception as e:
        await ctx.respond(f"```Parece que hubo un error al comunicarme con la API de GPT-j 🤒.\nNo te preocupes. En breves estáre disponible de nuevo.```")

    


bot.run("")
