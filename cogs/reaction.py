import discord
from discord.ext import commands

class Reaction(commands.Cog):

    def __init__(self, client):
        self.client = client

    # @client.command()
    # async def reaction(self, subcommand = None, channel : discord.TextChannel = None, message : discord.Message = None):
    #     pass

def setup(client):
    client.add_cog(Reaction(client))