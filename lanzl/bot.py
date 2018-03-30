import sys
import logging
from datetime import datetime
import asyncio
import atexit

import discord
from discord.ext import commands

from .utils import ConfigManager, HelpFormatter

MODULES = [
    "suggestions_board"
]


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

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user} with ID: {self.user.id}")
        await self.change_presence(game=discord.Game(name="~help for commands!", type=0))

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
