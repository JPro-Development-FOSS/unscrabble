import random
import functools
import operator
import itertools
from enum import Enum

COLS = 15
ROWS = COLS
LETTER_TO_POINT = {
        ' ': 0,
        'E': 1, 'A': 1, 'I': 1, 'O': 1, 'N': 1, 'R': 1, 'T': 1, 'L': 1, 'S': 1, 'U': 1,
        'D': 2, 'G': 2,
        'B': 3, 'C': 3, 'M': 3, 'P': 3,
        'F': 4, 'H': 4, 'V': 4, 'W': 4, 'Y': 4,
        'K': 5,
        'J': 8,
        'X': 8,
        'Q': 10, 'Z': 10,
        }

class Letter:
    def __init__(self, letter):
        self.letter = letter
        self.points = LETTER_TO_POINT[letter]

    def __str__(self):
        return '-' if self.letter is None else self.letter


class Spot:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.letter = None

    def __str__(self):
        return str(self.letter) if self.letter else '-'

class Board:
    def __init__(self, spots):
        self.spots = spots

    def empty(self):
        return functools.reduce(operator._or, [spot.letter for spot in self.spots])
    
    def __str__(self):
        out = ''
        for row in self.spots:
            out += ' '.join(["{}".format(spot) for spot in row]) + '\n'
        return out

class Bag:
    def __init__(self):
        self.bag = (
                [Letter(' ')] * 2 +
                [Letter('E')] * 12 +
                [Letter('A')] * 9 +
                [Letter('I')] * 9 +
                [Letter('O')] * 8 +
                [Letter('N')] * 6 +
                [Letter('R')] * 6 +
                [Letter('T')] * 6 +
                [Letter('L')] * 4 +
                [Letter('S')] * 4 +
                [Letter('U')] * 4 +
                [Letter('D')] * 4 +
                [Letter('G')] * 3 +
                [Letter('B')] * 2 +
                [Letter('C')] * 2 +
                [Letter('M')] * 2 +
                [Letter('P')] * 2 +
                [Letter('F')] * 2 +
                [Letter('H')] * 2 +
                [Letter('V')] * 2 +
                [Letter('W')] * 2 +
                [Letter('Y')] * 2 +
                [Letter('K')] * 1 +
                [Letter('J')] * 1 +
                [Letter('X')] * 1 +
                [Letter('Q')] * 1 +
                [Letter('Z')] * 1
            )
        random.shuffle(self.bag)

    def draw(self):
        return self.bag.pop()

class Game:
    def __init__(self, board, bag, players):
        self.board = board
        self.bag = bag
        self.players = players
        # TODO: this should really be whover draws the lowest letter from the bag
        self.turn = 0

    def next_player(self):
        self.turn = (self.turn + 1) % len(self.players)
        return self.players[self.turn]

    def __str__(self):
        return '{}\n{}'.format(
                self.board,
                '\n'.join(['{} p{}: {}'.format('*' if i == self.turn else ' ', i, p) for (i, p) in enumerate(self.players)]))

class WordDirection(Enum):
    RIGHT = 0
    DOWN = 1

class Player:
    def __init__(self, board, bag):
        self.board = board
        self.bag = bag
        self.letters = [bag.draw() for _ in range(7)]

    def do_the_thing(self):
        # permutations of letters
        permutations = itertools.permutations(self.letters, len(self.letters))
        max_score = -1
        max_word = None
        max_i = -1
        max_j = -1
        # each viable board space as starting point
        for i in range(COLS):
            for j in range(ROWS):
                for permutation in permutations:
                    for l in range(len(permutation)):
                        # try words to the right
                        # try words down
                        # check dictionary
                        # score, record max
                        word = permutation[:l]
                        score = self.board.score(i, j, word, WordDirection.RIGHT)
                        if score > max_score:
                            max_score = score
                            max_word = word
                            max_i = i
                            max_j = j
                        score = self.board.score(i, j, word, WordDirection.DOWN)
                        if score > max_score:
                            max_score = score
                            max_word = word
                            max_i = i
                            max_j = j

        # if viable word exists, play it. else give up (for now)


    def __str__(self):
        return ' '.join([str(letter) for letter in self.letters])


def make_game():
    spots = [[Spot(i,j) for j in range(0,COLS)] for i in range(0,ROWS)]
    board = Board(spots)
    bag = Bag()
    players = [Player(board, bag) for _ in range(2)]
    return Game(board, bag, players)

if __name__ == '__main__':
    spots = [[Spot(i,j) for j in range(0,COLS)] for i in range(0,ROWS)]
    board = Board(spots)
    bag = Bag()
    players = [Player(board, bag) for _ in range(2)]
    game = Game(board, bag, players)
    print(game)
