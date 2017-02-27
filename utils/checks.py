from discord.ext import commands
import discord
import json

with open("config/config.json") as data:
    config = json.load(data)
data.close()

# Checks if it is bot owner
def is_owner(ctx):
    return ctx.message.author.id == config["owner"]

# Checks if user is an admin
def is_admin(ctx):
    if is_owner(ctx):
        return True
    message = ctx.message
    channel = message.channel
    perms = channel.permissions_for(message.author)
    return perms.administrator

# Checks specific permissions
def perm_manage_roles(ctx):
    if is_owner(ctx):
        return True
    message = ctx.message
    channel = message.channel
    perms = channel.permissions_for(message.author)
    return perms.manage_roles

def perm_manager_server(ctx):
    if is_owner(ctx):
        return True
    message = ctx.message
    channel = message.channel
    perms = channel.permissions_for(message.author)
    return perms.manage_server

def perm_manage_messages(ctx):
    if is_owner(ctx):
        return True
    message = ctx.message
    channel = message.channel
    perms = channel.permissions_for(message.author)
    return perms.manage_messages

def perm_manage_channels(ctx):
    if is_owner(ctx):
        return True
    message = ctx.message
    channel = message.channel
    perms = channel.permissions_for(message.author)
    return perms.manage_channels

def perm_ban(ctx):
    if is_owner(ctx):
        return True
    message = ctx.message
    channel = message.channel
    perms = channel.permissions_for(message.author)
    return perms.ban_members

def perm_kick(ctx):
    if is_owner(ctx):
        return True
    message = ctx.message
    channel = message.channel
    perms = channel.permissions_for(message.author)
    return perms.kick_members
