import discord
import asyncio
import properties
import urllib.request
import json

client = discord.Client()
giphyApiBase = "http://api.giphy.com/v1/gifs/"
giphyApiKey = properties.giphyToken

def getJson(url):
    response = urllib.request.urlopen(url)
    data = json.load(response)
    return data    

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.lower() == '!neat':
        response = '<@' + message.author.id + '> NEAT!'
        await client.send_message(message.channel, response)
    elif message.content.lower() == 'hey neatbot':
        gifData =  getJson(giphyApiBase + "random?api_key=" + giphyApiKey + "&tag=hello&rating=G")             
        response = gifData["data"]["url"]
        await client.send_message(message.channel, response)



client.run(properties.token)
