import discord
from discord.ext import commands
import aiohttp
import os
from models.logger import setup_discord_logger as setup_logger

#bot = .Bot()
intents = discord.Intents.default()
#intents.members = True
intents.guilds = True
intents.emojis = True
intents.messages = True
intents.reactions = True
intents.presences = True

logger = setup_logger("logs/gpt.log")

bot = commands.Bot(command_prefix='=', intents=intents)
bot.remove_command('help')

db = {}
english_db = {}

@bot.event
async def on_ready():
    logger.info(f"Bot started as {bot.user.name} [{bot.user.id}]")

@bot.slash_command(name = "gpt", description = "Envíale un mensaje en español a GPT-j")
async def gpt(ctx, prompt: str):
    global db
    base_prompt = "¡Buen Día!. Me llamo GPT-j y soy un bot que pertenece al Servidor de Discord de DotCSV. Puede hacerme la pregunta que quieras, o simplemente puedes charlar conmigo"
    await generate_with_base_prompt(ctx, base_prompt, prompt, db)


@bot.slash_command(name = "english-gpt", description = "Envíale un mensaje en inglés a GPT-j")
async def gpt_ingles(ctx, prompt: str):
    global english_db
    base_prompt = "¡Hello there!. My name is GPT-j and I am a bot that works on DotCSV's Discord Server."
    await generate_with_base_prompt(ctx, base_prompt, prompt, english_db)
    

async def generate_with_base_prompt(ctx, base_prompt, prompt, db):

    await ctx.defer()
    new_prompt = make_prompt(ctx, base_prompt, prompt, db)
    payload = make_payload(new_prompt)
    response = await generate(ctx, payload)

    update_db(ctx, prompt, response, db)

    await ctx.respond(f"**Input:**\n```{prompt}```\n**Output:**\n```{response}```")


@bot.slash_command(name = "clear-input", description = "Limpia el input a GPT-j")
async def clean_input(ctx):
    global db
    global english_db
    await ctx.defer()
    db.pop(ctx.author.id, None)
    english_db.pop(ctx.author.id, None)
    await ctx.respond(f"El input de {ctx.author.display_name} fue eliminado")



def make_prompt(ctx, base_prompt, prompt, prompt_db):

    new_prompt = f"BOT:{base_prompt}"
    if ctx.author.id in prompt_db:
        for p in prompt_db[ctx.author.id]:
            new_prompt += f"\n{ctx.author.display_name}: {p['prompt']}"
            new_prompt += f"\nBOT: {p['response']}"
            
    new_prompt += f"\n{ctx.author.display_name}: {prompt}"
    new_prompt += "\nBOT:"

    while (len(new_prompt) + 128) > 2048:
        new_prompt = new_prompt[1:]

    return new_prompt


async def generate(ctx, payload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("http://api.vicgalle.net:5000/generate", params=payload) as response:
                json_response = await response.json()            
    except Exception as e:
        await ctx.respond(f"```Parece que hubo un error al comunicarme con la API de GPT-j 🤒.\nNo te preocupes. En breves estáre disponible de nuevo.```")

    return json_response['text'].strip()

def make_payload(prompt):
    return {
        "context": prompt,
        "token_max_length": 128,
        "temperature": 1.0,
        "top_p": 0.9,
        "stop_sequence": "\n"
    }

def update_db(ctx, prompt, response, db):
    if ctx.author.id not in db.keys():
        db[ctx.author.id] = [{
            "prompt": prompt,
            "response": response
        }]
    else:
        db[ctx.author.id].append({
            "prompt": prompt,
            "response": response
        })


bot.run(os.environ['TOKEN'])
