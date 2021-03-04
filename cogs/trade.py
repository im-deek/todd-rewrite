import discord
from discord.ext import commands

class Trade(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def trade(self, command = None, value1 = None, value2 = None, value3 = None):



def setup(client):
    client.add_cog(Trade(client))