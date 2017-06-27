import asyncio
import discord
import json
import properties
import random
import sys
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

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    sys.stdout.flush()


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
    elif cmd == rollTriggerString:
        response = random.randint(1, 100)

    if response != "":
        await client.send_message(message.channel, response)

client.run(properties.token)