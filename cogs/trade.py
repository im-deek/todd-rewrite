import discord
from discord.ext import commands
from pymongo import MongoClient
from utils import myfunctions
import os

cluster = MongoClient(os.environ.get("TODD_MONGO"))
database = cluster["todd-data"]
collection = database["guildinfo"]

class Trade(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def trade(self, ctx, command = None, value1 = None, value2 = None, value3 = None):
        # planned commands: channel, add, close, remove
        if command == "auth" and ctx.author.id == 321732493764067329:

            guild = ctx.guild
            results = collection.find({"guild": guild.id})

            if value1 == None or value1.lower() == "false":
                auth = False
            elif value1.lower() == "true":
                auth = True

            if not list(results):
                all = collection.find({})
                total = len(list(all))
                collection.insert_one({"_id": guild.id, "name": guild.name, "trading": auth})
            else:
                collection.update_one({"_id": guild.id}, {"$set": {"trading": auth}})

            response = discord.Embed(title="Trading status updated", description=f"Changed to `{auth}`")
            await ctx.send(embed=response)





def setup(client):
    client.add_cog(Trade(client))
