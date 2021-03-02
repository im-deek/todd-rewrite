def getprefix(guildid):

    from pymongo import MongoClient

    cluster = MongoClient("mongodb+srv://Deek:6nTchtyLR5DUb9I8@todd.cprq1.mongodb.net/todd-data?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
    database = cluster["todd-data"]
    collection = database["prefix"]

    results = collection.find({"guild":guildid})
    for result in results:
        currentPrefix = result["prefix"]
        return currentPrefix
    return "$"
