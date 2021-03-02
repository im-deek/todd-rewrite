import discord
from discord.ext import commands, tasks
import os
from utils import myfunctions
import json
from itertools import cycle

# Flask Thing That Keeps It On

from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def main():
    return "Your Bot Is Ready"


def run():
    app.run(host="0.0.0.0", port=8000)


def keep_alive():
    server = Thread(target=run)
    server.start()


# Prefix finder and other things


async def determine_prefix(client, message):
    guild = message.guild.id
    if guild:
        return myfunctions.getprefix(guild)
    else:
        return "$"


client = commands.Bot(command_prefix=determine_prefix)
client.remove_command("help")

# Commands


@client.command()
async def ping(ctx):
    response = discord.Embed(title="Pong!",
                             colour=discord.Colour.from_rgb(153, 153, 255))
    response.description = f"Latency is {round(client.latency * 1000)}ms."
    await ctx.send(embed=response)


@client.command()
async def help(ctx):
    with open("help.json") as file:
        help = json.load(file)

    response = discord.Embed(title="Help Documentation",
                             colour=discord.Colour.gold())
    response.description = (
        "These are all the commands for Todd. If an argument is surrounded by [] then it is"
        " required, however arguments surrounded by {} are optional.")
    for command in help["help"]:
        response.add_field(name=command["command"],
                           value=command["description"])
    response.set_footer(text="Written by Deek")
    await ctx.send(embed=response)


# Events


@client.event
async def on_ready():
    print("ToddRewritten is online.")
    change_status.start()


@client.event
async def on_message(message):
    if client.user.mentioned_in(message):

        prefix = myfunctions.getprefix(message.guild.id)
        response = discord.Embed(title="Hey!",
                                 colour=discord.Colour.from_rgb(102, 255, 255))
        response.description = ("I am Todd, nice to meet you.")
        response.add_field(name="Prefix",
                           value=f"The current prefix is `{prefix}`")
        await message.channel.send(embed=response)
    else:
        await client.process_commands(message)


# A background task I need to make it stay online :/

status = cycle(["the chat", "the chat"])


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=next(status)))


# @client.event
# async def on_guild_join(guild):
# default = guild.default_role
# for channel in guild.text_channels:
#     if channel.permissions_for(default).send_messages
#         prefix = myfunctions.getprefix(guild.id)
#         response = discord.Embed(title="Hi there, I am Todd.", colour=discord.Colour.gold())
#         response.description = (f"Thanks for adding me to your server, to see what I can do type `{prefix}help`. "
#                                 f"\nI hope you find me useful and I look foward to serving this guild.")
#         response.set_footer(text="Written by Deek")
#         await channel.send(embed=response)
#     break

# Cogs


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")


for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        client.load_extension(f"cogs.{file[:-3]}")

client.run(os.environ.get('TODDTOKEN'))
