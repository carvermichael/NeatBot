import unittest
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import bookService as b

testBookName = "My favorite book"
containsErrorMessage = "{0} not contained in the response. Response: {1}"

def scrubData():
    b.saveDataJson(b.files.books, {})
    b.saveDataJson(b.files.members, {})

class TestBookService(unittest.TestCase):

    def test_AddBook(self):
        scrubData()

        expected = b.returnMessages.bookAdded.format(testBookName)
        actual = b.addBookToList(testBookName)
        self.assertEqual(expected, actual)
        
        expected = b.returnMessages.bookInList.format(testBookName)
        actual = b.addBookToList(testBookName)
        self.assertEquals(expected, actual)

    def test_removeBook(self):
        scrubData()
        b.addBookToList(testBookName)
        
        expected = b.returnMessages.bookRemoved.format(testBookName)
        actual = b.removeBookFromList(testBookName)
        self.assertEquals(expected, actual)
        
        expected = b.returnMessages.bookNotInList.format(testBookName)
        actual = b.removeBookFromList(testBookName)
        self.assertEquals(expected, actual)

    def test_assignBook(self):
        scrubData()
        
        expected = b.returnMessages.bookAssigned.format(testBookName, "Ethan")
        actual = b.assignBook(testBookName, "Ethan")
        self.assertIn(expected, actual)

    def test_assignRandomBook(self):
        scrubData()
        b.addBookToList(testBookName)
        b.addBookToList("testBook2")

        expected1 = b.returnMessages.bookAssigned.format(testBookName, "Ethan")
        expected2 = b.returnMessages.bookAssigned.format("testBook2", "Ethan")
        actual = b.assignRandomBook("Ethan")

        try: 
            self.assertIn(expected1, actual)
        except AssertionError:
            expectedFragment = "'{0}' and '{1}' are".format(expected1, expected2)
            responseFragment = "'{0}'".format(actual)
            assertErrorMessage = containsErrorMessage.format(expectedFragment, responseFragment)
            self.assertIn(expected2, actual, assertErrorMessage)

    def test_getAssignedBook(self):
        scrubData()
        b.assignBook(testBookName, "Ethan")

        expected = b.returnMessages.assignedBook.format("Ethan", testBookName)
        actual = b.getAssignedBook("Ethan")
        self.assertEquals(expected, actual)

    def test_getAllAssignedBooks(self):
        scrubData()
        b.assignBook(testBookName, "Ethan")
        b.assignBook("otherBook1", "Z")
        b.assignBook("", "Gambit")

        expected1 = "Ethan is currently reading {0}.\n".format(testBookName)
        expected2 = "Z is currently reading otherBook1.\n"
        expected3 = "Gambit has no book club book.\n"
        expected = [expected1, expected2, expected3]
        actual = b.getAllAssignedBooks()
        self.assertNotIn(False, [exp in actual for exp in expected])

    def test_listBooks(self):
        scrubData()
        b.addBookToList(testBookName)
        b.addBookToList("another book")
        b.addBookToList("one more book")

        expected1 = testBookName + '\n'
        expected2 = "another book\n"
        expected3 = "one more book\n"
        expected = [expected1, expected2, expected3]
        actual = b.listBooks()
        self.assertNotIn(False, [exp in actual for exp in expected])
    
    def test_unassignBook(self):
        scrubData()
        b.assignBook(testBookName, "Ethan")

        expected = b.returnMessages.bookUnassigned.format(testBookName, "Ethan")
        actual = b.unassignBook("Ethan")
        self.assertEquals(expected, actual)

if __name__ == '__main__':
    unittest.main()