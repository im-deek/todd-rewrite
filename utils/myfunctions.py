def getprefix(guildid):

    from pymongo import MongoClient
    import os

    cluster = MongoClient(os.environ.get("TODD_MONGO"))
    database = cluster["todd-data"]
    collection = database["guildinfo"]

    results = collection.find({"_id":guildid})
    for result in results:
        try:
            currentPrefix = result["prefix"]
            return currentPrefix
        except:
            pass
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
