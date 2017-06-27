import asyncio
import discord
import json
import properties
import random
import urllib.request

client = discord.Client()
giphyApiBase = "http://api.giphy.com/v1/gifs/"
giphyApiKey = properties.giphyToken
gifTriggerString= "gif me"
rollTriggerString = "!roll"
topTrendingGifTrigger = "top trending gif"

def getJson(url):
    response = urllib.request.urlopen(url)
    data = json.load(response)
    return data    

def getGif(searchTerm):
    gifData = getJson(giphyApiBase + "random?api_key=" + giphyApiKey + "&tag="+searchTerm+"&rating=G")
    gifUrl = gifData["data"]["url"]
    return gifUrl

def getTrendingGif(gifNumber, maxRecords):
    gifData = getJson(giphyApiBase + "trending?api_key="+giphyApiKey+"&limit="+maxRecords+"&rating=G")
    gifUrl = gifData["data"][gifNumber]["url"]
    return gifUrl

def roll(maxRoll):
    return random.randint(1, maxRoll)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    response = ""
    cmd = message.content.lower()

    if cmd == '!neat':
        response = '<@' + message.author.id + '> NEAT!'
    elif cmd == 'hey neatbot':
        response = getGif("hello")
    elif cmd.startswith(gifTriggerString):
        searchTerm = ""
        if len(message.content) > len(gifTriggerString):
            searchTerm = message.content[len(gifTriggerString):].lstrip()
        response = getGif(searchTerm)
    elif cmd.startswith(topTrendingGifTrigger):
        response = getTrendingGif(0, "1")
    elif cmd.startswith(rollTriggerString):
        maxRoll = 100
        if (len(message.content) > len(rollTriggerString)):
            maxRoll = int(cmd[len(rollTriggerString):].lstrip())

        response = roll(maxRoll)
    elif cmd == 'randomwinner':
        activeMembers = []
        for member in client.get_all_members():
            if member.status == discord.Status.online and member.name != 'NeatBot':
                activeMembers.append(member)

        highRoll = 0
        winner = ""
        for member in activeMembers:
            currRoll = roll(100)
            if currRoll > highRoll:
                highRoll = currRoll
                winner = member.name

        response = winner + " wins with a roll of " + str(highRoll)

    if response != "":
        await client.send_message(message.channel, response)

client.run(properties.token)