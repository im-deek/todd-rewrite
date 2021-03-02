def getprefix(guildid):

    from pymongo import MongoClient
    import os

    cluster = MongoClient(os.environ.get("TODDMONGOPREFIX"))
    database = cluster["todd-data"]
    collection = database["prefix"]

    results = collection.find({"guild":guildid})
    for result in results:
        currentPrefix = result["prefix"]
        return currentPrefix
    return "$"
