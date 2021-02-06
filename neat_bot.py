import discord
import json
import properties
import random
import urllib.request
import bookService
import gameService

client = discord.Client()
giphyApiBase = "http://api.giphy.com/v1/gifs/"
giphyApiKey = properties.giphyToken

memberToNotify = "snacks#7277"
fillScreenImageUrl = "https://i.imgur.com/jlFXbsF.png"
aw_yeahUrl = "https://media1.giphy.com/media/3nozJyPYl195u/giphy.gif"

botName = "neatbot"

#Triggers
class Triggers:
    gifTriggerString = "gif me"
    notifyTriggerString = "pubg"
    rollTriggerString = "!roll"
    topTrendingGifTrigger = "top trending gif"
    randomTrendingGifTrigger = "random trending gif"


#Files - These are used to track state
memberDataFile = "memberData.json"
bookDataFile = "data.json"

def getActiveMembers():
    activeMembers = []
    for member in client.get_all_members():
        if member.status == discord.Status.online and not member.bot:
            activeMembers.append(member)
    return activeMembers


def getJson(url):
    response = urllib.request.urlopen(url)
    data = json.load(response)
    return data


def getGif(searchTerm):
    params = urllib.parse.urlencode({"tag":searchTerm,"rating":"G"})
    gifData = getJson(giphyApiBase + "random?api_key=" + giphyApiKey + "&" + params)
    gifUrl = gifData["data"]["url"]
    return gifUrl


def getTrendingGif(gifNumber, maxRecords):
    params = urllib.parse.urlencode({"limit":maxRecords,"rating":"G"})
    gifData = getJson(giphyApiBase + "trending?api_key=" + giphyApiKey + "&" + params)
    gifUrl = gifData["data"][gifNumber]["url"]
    return gifUrl


def getRandomTrendingGif():
    trendingGifNumber = random.randint(1, 100) - 1
    return getTrendingGif(trendingGifNumber, 100)


def roll(maxRoll):
    return random.randint(1, maxRoll)

def help():
    keys = [i for i in Triggers.__dict__.keys() if i[:1] != '_']
    return [Triggers.__dict__[x] for x in keys]

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.author.bot:
        return

    userName = message.author.name
    response = ""
    cmd = message.content.lower()

    if cmd == 'hey ' + botName:
        response = getGif("hello")
    elif cmd == 'aw_yeah':
        response = aw_yeahUrl
    elif cmd.startswith(Triggers.gifTriggerString):
        searchTerm = ""
        if len(message.content) > len(Triggers.gifTriggerString):
            searchTerm = message.content[len(Triggers.gifTriggerString):].lstrip()
        response = getGif(searchTerm)
    elif cmd.startswith(Triggers.topTrendingGifTrigger):
        response = getTrendingGif(0, "1")
    elif cmd.startswith(Triggers.randomTrendingGifTrigger):
        response = getRandomTrendingGif()
    elif cmd.startswith(Triggers.rollTriggerString):
        maxRoll = 100
        if (len(message.content) > len(Triggers.rollTriggerString)):
            maxRoll = int(cmd[len(Triggers.rollTriggerString):].lstrip())

        response = roll(maxRoll)
    elif cmd == 'randomwinner':
        highRoll = 0
        winner = ""
        for member in getActiveMembers():
            currRoll = roll(100)
            if currRoll > highRoll:
                highRoll = currRoll
                winner = member.name

        response = winner + " wins with a roll of " + str(highRoll)
    elif cmd == 'fillscreen':
        response = fillScreenImageUrl
    elif Triggers.notifyTriggerString in cmd:
        channel = message.channel
        member = channel.server.get_member_named(memberToNotify)
        # Only notify if the member is offline
        if member not in getActiveMembers():
            await message.channel.send(member, 'PUBG was mentioned in ' + channel.name)
    elif cmd.startswith(bookService.Triggers.addBookTrigger):
        if len(message.content) > len(bookService.Triggers.addBookTrigger):
            bookName = message.content[len(bookService.Triggers.addBookTrigger):].lstrip()
            response = bookService.addBookToList(bookName)
    elif cmd == bookService.Triggers.listBooksTrigger:
        response = bookService.listBooks()
    elif cmd.startswith(bookService.Triggers.removeBookTrigger):
        if len(message.content) > len(bookService.Triggers.removeBookTrigger):
            bookName = message.content[len(bookService.Triggers.removeBookTrigger):].lstrip()
            response = bookService.removeBookFromList(bookName)
    elif cmd.startswith(bookService.Triggers.assignBookTrigger):
        if len(message.content) > len(bookService.Triggers.assignBookTrigger):
            bookName = message.content[len(bookService.Triggers.assignBookTrigger):].lstrip()
            response = bookService.assignBook(bookName, userName)
    elif cmd == bookService.Triggers.assignRandomBookTrigger:
        response = bookService.Triggers.bookService.assignRandomBook(userName)
    elif cmd == bookService.Triggers.unassignBookTrigger:
        response = bookService.unassignBook(userName)
    elif cmd == bookService.Triggers.getMyBookTrigger:
        response = bookService.getAssignedBook(userName)
    elif cmd == bookService.Triggers.getAllBooksTrigger:
        response = bookService.getAllAssignedBooks()
    elif "help" in cmd and "book" in cmd:
        response = bookService.bookHelp()
    elif cmd.startswith(botName) and "help" in cmd:
        response = bookService.bookHelp() + help() + gameService.gameHelp()
    #gameService
    elif cmd.startswith(gameService.Triggers.addGameTrigger):
        if len(message.content) > len(gameService.Triggers.addGameTrigger):
            gameName = message.content[len(gameService.Triggers.addGameTrigger):].lstrip()
            response = gameService.addGameToList(gameName)
    elif cmd.startswith(gameService.Triggers.removeGameTrigger):
        if len(message.content) > len(gameService.Triggers.removeGameTrigger):
            gameName = message.content[len(gameService.Triggers.removeGameTrigger):].lstrip()
            response = gameService.removeGameFromList(gameName)
    elif cmd.startswith(gameService.Triggers.listGamesTrigger):
        if len(message.content) > len(gameService.Triggers.listGamesTrigger):
            response = gameService.listGames()
    elif cmd.startswith(gameService.Triggers.gameHelp):
        response = gameService.gameHelp()
    if response != "":
        await message.channel.send(response)


@client.event
async def on_member_update(before, after):
    response = ""

    # The member started or changed games
    # if before.game is None and after.game is not None:
        # Disabling the response for now to avoid annoyance
        #response = "Hey " + after.name + ", have fun playing " + after.game.name + ". Thanks for inviting the rest of us."

    if response != "":
        #this doesn't work with discord > 1 - I'm not sure it's used, kinda assuming not due to the server name? funny, haha?
        await client.send_message(
            discord.utils.get(client.get_all_channels(), server__name='Steamy Pile', name='general'), response)

client.run(properties.neatbotToken)
