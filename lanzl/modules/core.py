import datetime
import subprocess
import inspect

import discord
from discord.ext import commands

from ..utils import ConfigManager
from .. import Cog


class Core(Cog):

    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot
        self.config = ConfigManager("core.json")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong")

    @commands.is_owner()
    @commands.command()
    async def update(self, ctx):
        """
        Updates the bot from the Github repo
        """
        await ctx.send("Calling process to update! :up: :date: ")
        try:
            done = subprocess.run("git pull", shell=True, stdout=subprocess.PIPE, timeout=30)
            if done:
                message = done.stdout.decode()
                await ctx.send("`{}`".format(message))
                if message == "Already up-to-date.\n":
                    await ctx.send("No update available :no_entry:")
                else:
                    await ctx.send("Succesfully updated! Rebooting now :repeat: ")
                    await self.bot.logout()
        except subprocess.CalledProcessError:
            await ctx.send("Error updating! :exclamation: ")
        except subprocess.TimeoutExpired:
            await ctx.send("Error updating - Process timed out! :exclamation: ")

    @commands.is_owner()
    @commands.command()
    async def eval(self, ctx, *, code):
        """
        Evaluates a line of code provided
        """
        code = code.strip("` ")
        try:
            result = eval(code)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await ctx.send("```py\nInput: {}\n{}: {}```".format(code, type(e).__name__, e))
        else:
            await ctx.send("```py\nInput: {}\nOutput: {}\n```".format(code, result))
        await ctx.message.delete()


setup = Core.setup
