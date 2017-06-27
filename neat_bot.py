import discord
import asyncio
import properties
import urllib.request
import json

client = discord.Client()
giphyApiBase = "http://api.giphy.com/v1/gifs/"
giphyApiKey = properties.giphyToken
gifTriggerString= "gif me"
topTrendingGifTrigger = "top trending gif"

def getJson(url):
    response = urllib.request.urlopen(url)
    data = json.load(response)
    return data    

def getGif(searchTerm):
    gifData = getJson(giphyApiBase + "random?api_key=" + giphyApiKey + "&tag="+searchTerm+"&rating=R")
    gifUrl = gifData["data"]["url"]
    return gifUrl

def getTrendingGif(gifNumber, maxRecords):
    gifData = getJson(giphyApiBase + "trending?api_key="+giphyApiKey+"&limit="+maxRecords+"&rating=R")
    gifUrl = gifData["data"][gifNumber]["url"]
    return gifUrl

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    response = ""
    if message.content.lower() == '!neat':
        response = '<@' + message.author.id + '> NEAT!'
    elif message.content.lower() == 'hey neatbot':
        response = gitGif("hello")
    elif message.content.startswith(gifTriggerString):
        searchTerm = ""
        if len(message.content) > len(gifTriggerString):
            searchTerm = message.content[len(gifTriggerString):].lstrip()
        response = getGif(searchTerm)
    elif message.content.startswith(topTrendingGifTrigger):
        response = getTrendingGif(0, "1")

    if response != "":
        await client.send_message(message.channel, response)


client.run(properties.token)
