import sys
import logging
from datetime import datetime
import asyncio
import atexit
import os

import discord
from discord.ext import commands

from .utils import ConfigManager, HelpFormatter


class LanzlOrbiter(commands.AutoShardedBot):

    def __init__(self):
        self.config = ConfigManager("bot_config.json")
        super().__init__(
            command_prefix=self.config["prefix"],
            description="Lanzl Orbitter",
            pm_help=True,
            formatter=HelpFormatter()
        )
        self.logger = logging.getLogger(__name__)
        self.startup = None

    @property
    def uptime(self):
        return datetime.now() - self.startup

    async def on_command(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            self.logger.debug(f"Command: '{ctx.command}' "
                              f"User: '{ctx.author}'/{ctx.author.id} (In DM's)")
        else:
            self.logger.debug(f"Command: {ctx.command} "
                              f"Channel: '#{ctx.channel.name}'/{ctx.channel.id} "
                              f"Guild: '{ctx.guild}'/{ctx.guild.id} "
                              f"User: '{ctx.author}'/{ctx.author.id}")

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user} with ID: {self.user.id}")
        await self.change_presence(activity=discord.Game(name="~help for commands!"))

    def save_configs(self):
        self.config.save()
        for cog in self.cogs:
            self.cogs[cog].config.save()

    async def autosave(self):
        await self.wait_until_ready()
        while not self.is_closed():
            await self.save_configs()
            await asyncio.sleep(120)

    def run(self):
        atexit.register(self.save_configs)
        self.logger.info("Loading modules")
        for cog in self.config["modules"].keys():
            self.load_extension("lanzl.modules.{}".format(cog.lower()))
            self.logger.debug(f"Loaded module '{cog}'")
        self.logger.info("Finished loading modules")
        self.logger.info("Logging into Discord")
        try:
            super().run(self.config["discord_token"])
        except discord.errors.LoginFailure:
            self.logger.error("Improper token has been passed!")


def main():
    os.chdir("lanzl")
    logger = logging.getLogger("lanzl")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)8s [%(name)s] : %(message)s'))
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    LanzlOrbiter().run()


def __main__():
    main()


if __name__ == "__main__":
    main()
