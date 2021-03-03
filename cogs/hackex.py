import discord
from discord.ext import commands
import json
from utils import myfunctions
import requests
import os

# Limits requests to IPV4 only

import socket
import requests.packages.urllib3.util.connection as urllib3_cn


def allowed_gai_family():
    family = socket.AF_INET  # force IPv4
    return family


urllib3_cn.allowed_gai_family = allowed_gai_family

# Rest of cog

class Hackex(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hackex(self, ctx, command = None, value = None):
        colour = discord.Colour.from_rgb(0, 153, 255)

        if command == None:
            embed = myfunctions.gethelpdoc("hackexhelp.json")
            embed.colour=colour
            await ctx.send(embed=embed)

        elif command.lower() == "leaderboard":
            try:
                count = int(value)
                if count < 0:
                    count = 10
                elif count > 50:
                    count = 50
            except:
                count = 10

            api = os.environ.get("TODD_HACKEX_LB")
            apiResponse = (requests.get(api)).json()

            leaderboard = discord.Embed(title="HackEx Monthly Leaderboard")
            leaderboard.set_thumbnail(url="https://www.pcforecaster.com/wp-content/uploads/app_icons/hack-ex-simulator8578995.png")
            leaderboard.add_field(name=f"Top {count}", value="None")
            leaderboard.add_field(name="Level", value="None")

            names = ""
            levels = ""

            for i in range(0,count):
                player = apiResponse["curr_month_entries"][i]
                playerName = player["username"]
                playerLevel = player["level"]

                names += f"**{i+1}** {playerName}\n"
                levels += f"{playerLevel}\n"
                leaderboard.set_field_at(0, name=f"Top {count}", value=names, inline=True)
                leaderboard.set_field_at(1, name="Level", value=levels, inline=True)

            leaderboard.colour = colour
            await ctx.send(embed=leaderboard)

def setup(client):
    client.add_cog(Hackex(client))