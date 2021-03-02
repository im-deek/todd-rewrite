import discord
from discord.ext import commands
from random import randint

class Pp(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pp(self, ctx, user : discord.Member = None):
        if user == None:
            user = ctx.author

        size = randint(1,25)
        content = "8"
        for i in range(0,size):
            content = content+"="
        embed = discord.Embed(title=f"PP Size Measurer - {user.name}", description=content+"D", colour=discord.Colour.from_rgb(255,153,153))
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Pp(client))