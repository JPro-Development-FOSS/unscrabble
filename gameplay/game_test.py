import unittest
import timeit

from game import Player, WordLoader, Solver, WordDirection, Board, Game, Bag, Spot, ROWS, COLS, make_game, Letter

def place_word(word, board, i, j, word_direction):
    for letter in word:
        if word_direction == WordDirection.DOWN:
            while board.spots[i][j].letter != None:
                i += 1
            board.spots[i][j].letter = Letter(letter)
            i += 1
        else:
            while board.spots[i][j].letter != None:
                j += 1
            board.spots[i][j].letter = Letter(letter)
            j += 1


def letters(word):
    return [Letter(c) for c in word.upper()]

class TestGame(unittest.TestCase):
    def test_board(self):
        g = make_game()
        print(g)

    def test_solve(self):
        spots = [[Spot(i,j) for j in range(0,COLS)] for i in range(0,ROWS)]
        board = Board(spots)
        bag = Bag()
        player = Player(board, bag)
        print('\n')
        print('letters: {}'.format(str(player)))
        start = timeit.default_timer()
        word_loader = WordLoader('dictionary.txt')
        t = timeit.default_timer() - start
        print('{} words loaded in {}s'.format(len(word_loader.words), t))
        solver = Solver(word_loader.words)
        start = timeit.default_timer()
        solver.solve(board, player.letters)
        t = timeit.default_timer() - start
        print('solved in {}s'.format(t))

    def test_reaches(self):
        spots = [[Spot(i,j) for j in range(0,COLS)] for i in range(0,ROWS)]
        board = Board(spots)
        bag = Bag()
        player = Player(board, bag)
        self.assertFalse(board.reaches(4, 6, 7, WordDirection.DOWN))
        place_word('YEET', board, 7, 7, WordDirection.RIGHT)
        self.assertTrue(board.reaches(4, 6, 7, WordDirection.DOWN))

    def test_fits(self):
        spots = [[Spot(i,j) for j in range(0,COLS)] for i in range(0,ROWS)]
        board = Board(spots)
        bag = Bag()
        player = Player(board, bag)
        self.assertTrue(board.fits(4, 7, 7, WordDirection.RIGHT))
        place_word('YEET', board, 7, 7, WordDirection.RIGHT)
        self.assertTrue(board.fits(4, 7, 11, WordDirection.RIGHT))
        self.assertFalse(board.fits(5, 7, 11, WordDirection.RIGHT))
        self.assertTrue(board.fits(8, 6, 7, WordDirection.DOWN))
        print(board)
        self.assertFalse(board.fits(9, 6, 7, WordDirection.DOWN))

    def test_expand(self):
        spots = [[Spot(i,j) for j in range(0,COLS)] for i in range(0,ROWS)]
        board = Board(spots)
        bag = Bag()
        player = Player(board, bag)
        place_word('YEET', board, 7, 7, WordDirection.RIGHT)
        expanded = board.expand(letters('ER'), 7, 11, WordDirection.RIGHT)
        print([''.join([str(l) for l in w]) for w in expanded])
        self.assertEqual([letters('YEETER')], expanded)
        place_word('ER', board, 7, 11, WordDirection.RIGHT)
        expanded = board.expand(letters('EAT'), 6, 11, WordDirection.RIGHT)
        print([''.join([str(l) for l in w]) for w in expanded])
        place_word('EAT', board, 6, 11, WordDirection.RIGHT)
        print(board)
        self.assertEqual([letters('EE'), letters('AR'), letters('EAT')], expanded)
        expanded = board.expand(letters('TAS'), 4, 13, WordDirection.DOWN)
        print([''.join([str(l) for l in w]) for w in expanded])
        place_word('TAS', board, 4, 13, WordDirection.DOWN)
        print(board)
        self.assertEqual([letters('YEETERS'), letters('TATS')], expanded)

if __name__ == '__main__':
    unittest.main()
