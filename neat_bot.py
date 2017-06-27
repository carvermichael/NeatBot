import discord
import asyncio
import properties

client = discord.Client()


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


client.run(properties.token)
