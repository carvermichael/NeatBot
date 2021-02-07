import unittest
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import gameService as g

testGameName = "My favorite game"
containsErrorMessage = "{0} not contained in the response. Response: {1}"

def scrubData():
    g.saveDataJson(g.files.games, {})

class TestGameService(unittest.TestCase):

    def test_AddGame(self):
        scrubData()

        expected = g.returnMessages.gameAdded.format(testGameName)
        actual = g.addGameToList(testGameName)
        self.assertEqual(expected, actual)
        
        expected = g.returnMessages.gameInList.format(testGameName)
        actual = g.addGameToList(testGameName)
        self.assertEqual(expected, actual)

    def test_removeGame(self):
        scrubData()
        g.addGameToList(testGameName)
        
        expected = g.returnMessages.gameRemoved.format(testGameName)
        actual = g.removeGameFromList(testGameName)
        self.assertEqual(expected, actual)
        
        expected = g.returnMessages.gameNotInList.format(testGameName)
        actual = g.removeGameFromList(testGameName)
        self.assertEqual(expected, actual)


    def test_listGames(self):
        scrubData()
        g.addGameToList(testGameName)
        g.addGameToList("another book")
        g.addGameToList("one more book")

        expected1 = testGameName + '\n'
        expected2 = "another book\n"
        expected3 = "one more book\n"
        expected = [expected1, expected2, expected3]
        actual = g.listGames()
        self.assertNotIn(False, [exp in actual for exp in expected])


    def test_helpGame(self):
        scrubData()

        expected = ['list games', 'add game ', 'remove game ', 'game help']
        actual = g.gameHelp()

        for command in expected:
            assert command in actual


if __name__ == '__main__':
    unittest.main()