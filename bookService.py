import json
import random
import sys

class files:
    members = "memberData.json"
    books = "data.json"

class keys:
    books = "books"
    assigned = "assignedBook"

class returnMessages:
    bookAdded = "{0} added to book list."
    bookInList = "{0} already in book list."
    bookRemoved = "{0} removed from book list."
    bookNotInList = "{0} not in book list."
    bookAssigned = "{0} assigned to {1}."
    bookUnassigned = "{0} unassigned from {1}."
    assignedBook = "{0} is currently reading {1}."

class Triggers:
    # Book Triggers - These are used to call methods in the bookService
    listBooksTrigger = "list books"
    addBookTrigger = "add book "
    removeBookTrigger = "remove book "
    assignBookTrigger = "assign book "
    assignRandomBookTrigger = "assign random book"
    unassignBookTrigger = "unassign my book"
    getMyBookTrigger = "get my book"
    getAllBooksTrigger = "list all books"

def addBookToList(bookName):
    data = loadJsonFile(files.books, {})
    books = data.get(keys.books, [])

    if bookName in books:
        return returnMessages.bookInList.format(bookName)        

    books.append(bookName)
    data[keys.books] = books

    saveDataJson(files.books, data)

    return returnMessages.bookAdded.format(bookName)


def removeBookFromList(bookName):
    data = loadJsonFile(files.books, {})
    books = data.get(keys.books, [])

    if bookName in books:
        books.remove(bookName)
        data[keys.books] = books
        saveDataJson(files.books, data)
        return returnMessages.bookRemoved.format(bookName)
    else:
        return returnMessages.bookNotInList.format(bookName)

def listBooks():
    data = loadJsonFile(files.books, {})
    books = data.get(keys.books, [])

    response = ""
    if len(books) == 0:
        return "No books in list!"

    for book in books:
        response += book + '\n'

    return response

def assignBook(bookName, personName):
    memberData = loadJsonFile(files.members, {})
    memberInfo = memberData.get(personName, {})

    assignedBook = memberInfo.get(keys.assigned, "")
    response = ""
    if len(assignedBook) > 0:
        response = unassignBook(personName) + '\n'

    memberInfo[keys.assigned] = bookName
    memberData[personName] = memberInfo

    saveDataJson(files.members, memberData)

    response += returnMessages.bookAssigned.format(bookName, personName)

    return response

def assignRandomBook(personName):
    bookData = loadJsonFile(files.books, {})
    books = bookData.get(keys.books, [])

    if len(books) == 0:
        return "No books in book list to assign."
    
    memberData = loadJsonFile(files.members, {})
    memberInfo = memberData.get(personName, {})

    assignedBook = memberInfo.get(keys.assigned, "")

    randomBookNumber = random.randint(0, len(books) - 1)
    randomBookName = books[randomBookNumber]

    while randomBookName == assignedBook:
        randomBookNumber = random.randint(0, len(books) - 1)
        randomBookName = books[randomBookNumber]

    return assignBook(randomBookName, personName)

def unassignBook(personName):
    memberData = loadJsonFile(files.members, {})
    memberInfo = memberData.get(personName, {})
    assignedBook = memberInfo.get(keys.assigned, "")

    if len(assignedBook) == 0:
        return "No book currently assigned to {0}.".format(personName)

    memberInfo[keys.assigned] = ""
    memberData[personName] = memberInfo
    saveDataJson(files.members, memberData)
    return returnMessages.bookUnassigned.format(assignedBook, personName)

def getAssignedBook(personName):
    memberData = loadJsonFile(files.members, {})
    memberInfo = memberData.get(personName, {})

    assignedBook = memberInfo.get(keys.assigned, "")

    if len(assignedBook) == 0:
        return "{0} has no book club book.".format(personName)
    
    return returnMessages.assignedBook.format(personName, assignedBook) 

def getAllAssignedBooks():
    memberData = loadJsonFile(files.members, {})
    memberNames = memberData.keys()
    response = ""

    for memberName in memberNames:
        response += getAssignedBook(memberName) + "\n"

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

def bookHelp():
    keys = [i for i in Triggers.__dict__.keys() if i[:1] != '_']
    return [Triggers.__dict__[x] for x in keys]

