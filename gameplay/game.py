import random
import functools
import operator
import itertools
import pprint
from enum import Enum
from dataclasses import dataclass
from typing import Sequence

COLS = 15
ROWS = COLS
LETTER_TO_POINT = {
        '_': 0,
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

    def __eq__(self, other):
        return other != None and self.letter == other.letter


class Spot:
    def __init__(self, row, col, letter = None):
        self.row = row
        self.col = col
        self.letter = letter

    def __str__(self):
        return str(self.letter) if self.letter else '-'

    def __eq__(self, other):
        return other != None and self.row == other.row and self.col == other.col and self.letter == other.letter

class Board:
    def __init__(self, spots):
        self.spots = spots

    def empty(self):
        return functools.reduce(operator.and_, [spot.letter == None for row in self.spots for spot in row])

    def score(self, spotted_words, i, j, direction):
        # TODO: take multipliers and adjacent words into account
        return functools.reduce(operator.add, [spot.letter.points for word in spotted_words for spot in word])
   
    def reaches(self, num_letters, i, j, direction):
        if self.empty():
            if direction == WordDirection.RIGHT:
                return i == 7 and j <=7 and j+num_letters > 7 and j+num_letters < COLS
            if direction == WordDirection.DOWN:
                return j == 7 and i <=7 and i+num_letters > 7 and i+num_letters < ROWS
        else:
            for k in range(num_letters):
                if direction == WordDirection.RIGHT:
                    if j+k < COLS and self.spots[i][j+k].letter != None:
                        return True
                    if j+k < COLS and i > 0 and self.spots[i-1][j+k].letter != None:
                        return True
                    if j+k < COLS and i < ROWS-1 and self.spots[i+1][j+k].letter != None:
                        return True
                if direction == WordDirection.DOWN:
                    if i+k < ROWS and self.spots[i+k][j].letter != None:
                        return True
                    if i+k < ROWS and j > 0 and self.spots[i+k][j-1].letter != None:
                        return True
                    if i+k < ROWS and j < COLS-1 and self.spots[i+k][j+1].letter != None:
                        return True
            return False

    def fits(self, num_letters, i, j, direction):
        if self.spots[i][j].letter != None:
            return False
        remaining = COLS - num_letters
        if direction == WordDirection.RIGHT:
            remaining -= j
            for k in range(j, COLS):
                if self.spots[i][k].letter != None:
                    remaining -= 1
        if direction == WordDirection.DOWN:
            remaining -= i
            for k in range(i, ROWS):
                if self.spots[k][j].letter != None:
                    remaining -= 1
        return remaining >= 0

    def expand(self, letters, i, j, direction):
        def gather_up(i, j):
            k = 1
            gathered = []
            while i - k >= 0 and self.spots[i-k][j].letter != None:
                gathered.append(self.spots[i-k][j])
                k += 1
            return gathered
        def gather_down(i, j):
            k = 1
            gathered = []
            while i + k < ROWS and self.spots[i+k][j].letter != None:
                gathered.append(self.spots[i+k][j])
                k += 1
            return gathered
        def gather_left(i, j):
            k = 1
            gathered = []
            while j - k >= 0 and self.spots[i][j-k].letter != None:
                gathered.append(self.spots[i][j-k])
                k += 1
            return gathered
        def gather_right(i, j):
            k = 1
            gathered = []
            while j + k < COLS and self.spots[i][j+k].letter != None:
                gathered.append(self.spots[i][j+k])
                k += 1
            return gathered
        words=[]
        if direction == WordDirection.RIGHT:
            word = gather_left(i, j)
            word.reverse()
            k=0
            for letter in letters:
                while self.spots[i][j+k].letter != None:
                    word.append(self.spots[i][j+k])
                    k+=1
                # gather main word
                word.append(Spot(i, j+k, letter))
                # gather adjacent words
                up = gather_up(i, j+k)
                down = gather_down(i, j+k)
                if up or down:
                    up.reverse()
                    words.append(up + [Spot(i, j+k, letter)] + down)
                k+=1
            word += gather_right(i, j+k)
            words.append(word)
        if direction == WordDirection.DOWN:
            word = gather_up(i, j)
            word.reverse()
            k=0
            for letter in letters:
                while self.spots[i+k][j].letter != None:
                    word.append(self.spots[i+k][j])
                    k+=1
                # gather main word
                word.append(Spot(i+k, j, letter))
                # gather adjacent words
                left = gather_left(i+k, j)
                right = gather_right(i+k, j)
                if left or right:
                    left.reverse()
                    words.append(left + [Spot(i+k, j, letter)] + right)
                k+=1
            word += gather_down(i+k, j)
            words.append(word)

        # return list of lists of tiles with each list being a word that should
        # be scored. AKA the same tile could appear more than once.
        return words

    def __str__(self):
        out = ''
        for row in self.spots:
            out += ' '.join(["{}".format(spot) for spot in row]) + '\n'
        return out

class Bag:
    def __init__(self):
        self.bag = (
                [Letter('_')] * 2 +
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

class WordLoader:
    def __init__(self, path):
        self.words = set()
        with open(path, encoding="utf-8") as f:
            for line in f:
                self.words.add(line.strip())

@dataclass
class Solution:
    score: int = 0
    word: Sequence[Letter] = None
    word_str: str = ''
    i: int = 0
    j: int = 0
    direction: WordDirection = WordDirection.RIGHT

class Solver:
    def __init__(self, words):
        self.words = words

    def solve(self, board, letters):
        print('board empty: {}'.format(board.empty()))
        # only deal with letters
        print('{} letters'.format(len(letters)))
        count = 0
        solution = Solution()
        for i in range(ROWS):
            for j in range(COLS):
                permutations = itertools.permutations(letters, len(letters))
                for permutation in permutations:
                    count += 1
                    for l in range(1, len(permutation)):
                        word = permutation[:l]
                        word_str = ''.join(letter.letter for letter in word)
                        expanded = []
                        if (board.reaches(l, i, j, WordDirection.RIGHT) and
                            board.fits(l, i, j, WordDirection.RIGHT)):
                            expanded.append((board.expand(
                                word, i, j, WordDirection.RIGHT), WordDirection.RIGHT))
                        if (board.reaches(l, i, j, WordDirection.DOWN) and
                            board.fits(l, i, j, WordDirection.DOWN)):
                            expanded.append((board.expand(
                                word, i, j, WordDirection.DOWN), WordDirection.DOWN))
                        for spotted_words, direction in expanded:
                            all_are_words = True
                            word_str = None
                            for spotted_word in spotted_words:
                                expanded_word = ''.join([spot.letter.letter for spot in spotted_word])
                                word_str = expanded_word if word_str == None else word_str
                                all_are_words = all_are_words and expanded_word in self.words
                            score = board.score(spotted_words, i, j, direction)
                            if all_are_words and score > solution.score:
                                # TODO: make "played" word first class
                                solution = Solution(
                                        score = score, word = spotted_words[0],
                                        word_str = word_str, i = i, j = j,
                                        direction = direction)
        pprint.pprint(solution)
        return solution

class Player:
    def __init__(self, board, bag, solver=None):
        self.board = board
        self.bag = bag
        self.letters = [bag.draw() for _ in range(7)]
        self.solver = solver

    def take_turn(self):
        # TODO: need to know what spots are involved in solution
        # self.solver.solve(self.board, self.letters)
        pass

    def __str__(self):
        return ' '.join([str(letter) for letter in self.letters])


def make_game():
    spots = [[Spot(i,j) for j in range(0,COLS)] for i in range(0,ROWS)]
    board = Board(spots)
    bag = Bag()
    word_loader = WordLoader('dictionary.txt')
    solver = Solver(word_loader.words)
    players = [Player(board, bag, solver) for _ in range(2)]
    return Game(board, bag, players)

if __name__ == '__main__':
    spots = [[Spot(i,j) for j in range(0,COLS)] for i in range(0,ROWS)]
    board = Board(spots)
    bag = Bag()
    players = [Player(board, bag) for _ in range(2)]
    game = Game(board, bag, players)
    print(game)
