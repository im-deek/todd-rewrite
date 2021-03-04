def getprefix(guildid):

    from pymongo import MongoClient
    import os

    cluster = MongoClient(os.environ.get("TODD_MONGO_PREFIX"))
    database = cluster["todd-data"]
    collection = database["guildinfo"]

    results = collection.find({"guild":guildid})
    for result in results:
        currentPrefix = result["prefix"]
        return currentPrefix
    return "$"

def gethelpdoc(filename):

    import json
    import discord

    with open(filename) as file:
        help = json.load(file)

    response = discord.Embed(title=help["embed_title"])
    response.description = help["embed_desc"]
    for command in help["help"]:
        response.add_field(name=command["command"],
                           value=command["description"],
                           inline=True)
    response.set_footer(text="Written by Deek")
    return response
