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

# Error command for lookup

def lookuperror(reason, colour):
    unable = discord.Embed(title="HackEx Player Lookup")
    unable.description = reason
    unable.colour = colour
    return unable


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

            apiResponse = (requests.get(os.environ.get("TODD_HACKEX_LB"))).json()

            leaderboard = discord.Embed(title="HackEx Monthly Leaderboard")
            leaderboard.description = "Use `hackex lookup [player]` for more detailed data."
            leaderboard.set_thumbnail(url="https://www.pcforecaster.com/wp-content/uploads/app_icons/hack-ex-simulator8578995.png")
            leaderboard.add_field(name=f"Top {count}", value="None")
            leaderboard.add_field(name="Level", value="None")

            names, levels = "", ""

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

        elif command.lower() == "lookup":
            if value == None:
                reason = "You must specify a value to search for."
                await ctx.send(embed=lookuperror(reason, colour))
            else:
                searchTerm = value
                apiResponse = (requests.get(os.environ.get("TODD_HACKEX_LB"))).json()

                searching = True
                i = 0
                while searching:
                    player = apiResponse["curr_month_entries"][i]

                    if player["username"].lower() == searchTerm.lower():
                        stats = discord.Embed(title="HackEx Player Lookup")
                        stats.description = f"""Data for **{player["username"]}**"""
                        stats.set_thumbnail(url="https://www.pcforecaster.com/wp-content/uploads/app_icons/hack-ex-simulator8578995.png")
                        stats.add_field(name="Level", value=player["level"])
                        stats.add_field(name="Reputation", value=f"""{int(player["reputation"]):,d}""")
                        stats.add_field(name="Score", value=f"""{int(player["score"]):,d}""")

                        stats.colour = colour
                        await ctx.send(embed=stats)
                        searching = False

                    elif i == 99:
                        reason = f"I am unable to find **{searchTerm}** on the leaderboard."
                        await ctx.send(embed=lookuperror(reason, colour))
                        searching = False
                    i += 1

def setup(client):
    client.add_cog(Hackex(client))