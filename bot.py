import discord
from discord.ext import commands
import json
import logging
from utils import checks

description = "A Space Satellite Orbiting the planet Lanzl - https://github.com/DiNitride/LanzlOrbiter"

bot = commands.Bot(command_prefix="?", description=description, pm_help=True)

with open("config/config.json") as f:
    bot.config = json.load(f)

@bot.event
async def on_ready():
    print("-----------------------------------------")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("-----------------------------------------")
    bot.load_extension("modules.weather")
    await bot.change_presence(game=discord.Game(name="~~today"))


@bot.command(hidden=True)
@commands.check(checks.is_owner)
async def updateprofile():
    """Updates the bot's profile image"""
    # Loads and sets the bot's profile image
    with open("logo.jpg","rb") as logo:
        await bot.edit_profile(avatar=logo.read())


@bot.command(hidden=True)
@commands.check(checks.is_owner)
async def changename(*, name):
    await bot.edit_profile(username=name)

# login token
bot.run(bot.config["login_token"])


