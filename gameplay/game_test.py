import game
import unittest
import timeit

class TestGame(unittest.TestCase):
    def test_board(self):
        g = game.make_game()
        print(g)

    def test_solve(self):
        spots = [[game.Spot(i,j) for j in range(0,game.COLS)] for i in range(0,game.ROWS)]
        board = game.Board(spots)
        bag = game.Bag()
        player = game.Player(board, bag)
        print('\n')
        print('letters: {}'.format(str(player)))
        start = timeit.default_timer()
        word_loader = game.WordLoader('dictionary.txt')
        t = timeit.default_timer() - start
        print('{} words loaded in {}s'.format(len(word_loader.words), t))
        solver = game.Solver(word_loader.words)
        start = timeit.default_timer()
        solver.solve(board, player.letters)
        t = timeit.default_timer() - start
        print('solved in {}s'.format(t))
    


if __name__ == '__main__':
    unittest.main()
