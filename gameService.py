import json
import random
import sys

class files:
    games = "gameData.json"

class keys:
    games = "games"

class returnMessages:
    gameAdded = "{0} added to game list."
    gameInList = "{0} already in game list."
    gameRemoved = "{0} removed from game list."
    gameNotInList = "{0} not in game list."

class Triggers:
    # Book Triggers - These are used to call methods in the bookService
    listGamesTrigger = "list games"
    addGameTrigger = "add game "
    removeGameTrigger = "remove game "

def addGameToList(gameName):
    data = loadJsonFile(files.games, {})
    games = data.get(keys.games, [])

    if gameName in games:
        return returnMessages.gameInList.format(gameName)

    games.append(gameName)
    data[keys.games] = games

    saveDataJson(files.games, data)

    return returnMessages.gameAdded.format(gameName)


def removeGameFromList(gameName):
    data = loadJsonFile(files.games, {})
    games = data.get(keys.games, [])

    if gameName in games:
        games.remove(gameName)
        data[keys.games] = games
        saveDataJson(files.games, data)
        return returnMessages.gameRemoved.format(gameName)
    else:
        return returnMessages.gameNotInList.format(gameName)

def listGames():
    data = loadJsonFile(files.games, {})
    games = data.get(keys.games, [])

    response = ""
    if len(games) == 0:
        return "No games in list!"

    for game in games:
        response += game + '\n'

    return response

def loadJsonFile(fileName, defaultJson):
    x = defaultJson
    try:
        file = open(fileName, 'r')
        x = json.load(file)
    except IOError as e:
        print("e.errno: " + str(e.errno))
        if e.errno == 2:
            saveDataJson(fileName, x)
        else:
            print("Unexpected error loading file " + fileName + ".", sys.exc_info()[0])
            raise
    except:
        print("Unexpected error loading file " + fileName + ".", sys.exc_info()[0])
        raise


    return x

def saveDataJson(fileName, data):
    with open(fileName, 'w') as file:
        json.dump(data, file)

def gameHelp():
    keys = [i for i in Triggers.__dict__.keys() if i[:1] != '_']
    return [Triggers.__dict__[x] for x in keys]

