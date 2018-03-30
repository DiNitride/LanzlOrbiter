from discord.ext import commands


class BlankConfig:
    def save(self):
        pass


class Cog(object):

    def __init__(self, bot):
        self.bot = bot
        self.config = BlankConfig()

    @classmethod
    def setup(cls, bot: commands.AutoShardedBot):
        """
        Sets up the current cog.
        """
        instance = cls(bot)
        bot.add_cog(instance)
