from datetime import datetime
import asyncio

import discord
from discord.ext import commands

from .. import Cog
from ..utils import ConfigManager

EMOJIS = {
    "UP_ARROW": "\N{upwards black arrow}",
    "DOWN_ARROW": "\N{downwards black arrow}"
}





class Suggestions(Cog):

    def __init__(self, bot: commands.AutoShardedBot):
        super().__init__(bot)
        self.config = ConfigManager("suggestions_board.json")
        self.suggestions = {}

    @commands.group(invoke_without_command=True)
    async def suggestion(self, ctx, *, suggestion: str):
        """
        Make a suggestion for the server.
        """
        title_req = await ctx.send("**Thanks for your suggestion!** What would you like to title your post?")

        title = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author)

        embed = self.create_suggestion_embed(title.content, suggestion, ctx.author.id, 0, 0)

        resp = await self.bot.get_channel(self.config['suggestion_channel']).send(embed=embed)
        await resp.add_reaction(EMOJIS["UP_ARROW"])
        await resp.add_reaction(EMOJIS["DOWN_ARROW"])

        self.suggestions[resp.id] = {
            "title": title.content,
            "suggestion": suggestion,
            "author": ctx.author.id,
            "up": 0,
            "down": 0
        }

        resp = await ctx.send("Thank you for your suggestion, it has been added to the suggestion channel...")

        await asyncio.sleep(10)
        await ctx.message.delete()
        await title_req.delete()
        await title.delete()
        await resp.delete()

    @suggestion.group(invoke_without_command=True)
    async def channel(self, ctx):
        """
        Get's the suggestion channel for the guild.
        """
        if self.config["suggestion_channel"]:
            await ctx.send(f"`Suggestions are logged to `#{self.bot.get_channel(self.config['suggestion_channel'])}")
        else:
            await ctx.send(f"`This guild does not have server suggestions set up`")

    @channel.command()
    @commands.has_permissions(manage_guild=True)
    async def set(self, ctx):
        """
        Set's the suggestion channel for the guild.
        """
        self.config["suggestion_channel"] = ctx.channel.id
        await ctx.send(f"`Set the guild's suggestion channel to #{ctx.channel}`")

    @channel.command()
    @commands.has_permissions(manage_guild=True)
    async def clear(self, ctx):
        """
        Clears the suggestion channel for the guild
        """
        self.config["suggestion_channel"] = None
        await ctx.send("`Cleared the guild's suggestion channel`")

    def create_suggestion_embed(self, title, suggestion, author, up, down):
        author = self.bot.get_user(author)

        embed = discord.Embed(title=title, colour=discord.Colour.blue(), url="https://discordapp.com",
                              description=suggestion,
                              timestamp=datetime.now())

        embed.set_author(name=author, url="https://discordapp.com",
                         icon_url=author.avatar_url)

        embed.set_footer(text="Discuss this suggestion in #discussion!")

        embed.add_field(name="Updoots \N{upwards black arrow}", value=up, inline=True)
        embed.add_field(name="Downdoots \N{downwards black arrow}", value=down, inline=True)
        return embed

    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return
        msg = reaction.message
        if msg.id in self.suggestions:
            suggestion = self.suggestions[msg.id]
            if reaction.emoji == EMOJIS["UP_ARROW"]:
                suggestion["up"] += 1
                for r in msg.reactions:
                    if r.emoji == EMOJIS["DOWN_ARROW"] and await r.users().get(id=user.id):
                        await msg.remove_reaction(EMOJIS["DOWN_ARROW"], user)
            if reaction.emoji == EMOJIS["DOWN_ARROW"]:
                suggestion["down"] += 1
                for r in msg.reactions:
                    if r.emoji == EMOJIS["UP_ARROW"] and await r.users().get(id=user.id):
                        await msg.remove_reaction(EMOJIS["UP_ARROW"], user)
            self.suggestions[msg.id] = suggestion
            await msg.edit(embed=self.create_suggestion_embed(**self.suggestions[msg.id]))

    async def on_reaction_remove(self, reaction, user):
        if user == self.bot.user:
            return
        msg = reaction.message
        if msg.id in self.suggestions:
            suggestion = self.suggestions[msg.id]
            if reaction.emoji == EMOJIS["UP_ARROW"]:
                suggestion["up"] -= 1
            elif reaction.emoji == EMOJIS["DOWN_ARROW"]:
                suggestion["down"] -= 1
            self.suggestions[msg.id] = suggestion
            await msg.edit(embed=self.create_suggestion_embed(**self.suggestions[msg.id]))


setup = Suggestions.setup
