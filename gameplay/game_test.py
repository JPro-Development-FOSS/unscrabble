import game
import unittest

class TestGame(unittest.TestCase):
    def test_board(self):
        g = game.make_game()
        print(g)

if __name__ == '__main__':
    unittest.main()
