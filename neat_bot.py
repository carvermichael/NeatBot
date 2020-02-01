import discord
import json
import properties
import random
import urllib.request

client = discord.Client()
giphyApiBase = "http://api.giphy.com/v1/gifs/"
giphyApiKey = properties.giphyToken
gifTriggerString = "gif me"
notifyTriggerString = "pubg"
memberToNotify = "snacks#7277"
rollTriggerString = "!roll"
topTrendingGifTrigger = "top trending gif"
randomTrendingGifTrigger = "random trending gif"
fillScreenImageUrl = "https://i.imgur.com/jlFXbsF.png"
aw_yeahUrl = "https://media1.giphy.com/media/3nozJyPYl195u/giphy.gif"

listBooksTrigger = "list books"
addBookTrigger = "add book "
removeBookTrigger = "remove book "


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


def loadJsonFile():
    with open('data.json', 'r') as file:
        return json.load(file)


def saveDataJson(data):
    with open('data.json', 'w') as file:
        json.dump(data, file)


@client.event
def listBooks():
    data = loadJsonFile()
    books = data['books']

    response = ""
    for book in books:
        response += book + '\n'

    return response


@client.event
def addBook(bookName):
    data = loadJsonFile()
    books = data['books']

    books.append(bookName)
    data['books'] = books

    saveDataJson(data)

    return "Book Added"


@client.event
def removeBook(bookName):
    data = loadJsonFile()
    books = data['books']

    if bookName in books:
        books.remove(bookName)
        data['books'] = books
        saveDataJson(data)
        return "Book Removed"
    else:
        return "Book Not Found"


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

    response = ""
    cmd = message.content.lower()

    if cmd == 'hey neatbot':
        response = getGif("hello")
    elif cmd == 'aw_yeah':
        response = aw_yeahUrl
    elif cmd.startswith(gifTriggerString):
        searchTerm = ""
        if len(message.content) > len(gifTriggerString):
            searchTerm = message.content[len(gifTriggerString):].lstrip()
        response = getGif(searchTerm)
    elif cmd.startswith(topTrendingGifTrigger):
        response = getTrendingGif(0, "1")
    elif cmd.startswith(randomTrendingGifTrigger):
        response = getRandomTrendingGif()
    elif cmd.startswith(rollTriggerString):
        maxRoll = 100
        if (len(message.content) > len(rollTriggerString)):
            maxRoll = int(cmd[len(rollTriggerString):].lstrip())

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
    elif notifyTriggerString in cmd:
        channel = message.channel
        member = channel.server.get_member_named(memberToNotify)
        # Only notify if the member is offline
        if member not in getActiveMembers():
            await client.send_message(member, 'PUBG was mentioned in ' + channel.name)
    elif cmd.startswith(addBookTrigger):
        if len(message.content) > len(addBookTrigger):
            bookName = message.content[len(addBookTrigger):].lstrip()
            response = addBook(bookName)
    elif cmd == listBooksTrigger:
        response = listBooks()
    elif cmd.startswith(removeBookTrigger):
        if len(message.content) > len(removeBookTrigger):
            bookName = message.content[len(removeBookTrigger):].lstrip()
            response = removeBook(bookName)

    if response != "":
        await client.send_message(message.channel, response)


@client.event
async def on_member_update(before, after):
    response = ""

    # The member started or changed games
    # if before.game is None and after.game is not None:
        # Disabling the response for now to avoid annoyance
        #response = "Hey " + after.name + ", have fun playing " + after.game.name + ". Thanks for inviting the rest of us."

    if response != "":
        await client.send_message(
            discord.utils.get(client.get_all_channels(), server__name='Steamy Pile', name='general'), response)


client.run(properties.neatbotToken)
