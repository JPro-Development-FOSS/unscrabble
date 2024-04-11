import random
import functools
import operator
import itertools
import pprint
import timeit
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

    def __repr__(self):
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
        self.empty = True
        # TODO: reaches opt
        # self.reaches_valid = False
        # self.rows = len(spots)
        # self.cols = len(spots[0])
        # self.reaches_requred_length = [[-1 for j in range(0, self.cols)] for i in range(0, self.rows)]

    def set_letter(self, i, j, letter):
        self.spots[i][j].letter = letter
        self.empty = False
        # TODO: reaches opt
        # self.reaches_valid = False

    def score(self, spotted_words, i, j, direction):
        # TODO: take multipliers and adjacent words into account
        return functools.reduce(operator.add, [spot.letter.points for word in spotted_words for spot in word])
   
    def reaches(self, num_letters, i, j, direction):
        if self.empty:
            if direction == WordDirection.RIGHT:
                return i == 7 and j <=7 and j+num_letters > 7 and j+num_letters < COLS
            if direction == WordDirection.DOWN:
                return j == 7 and i <=7 and i+num_letters > 7 and i+num_letters < ROWS
        else:
            # TODO: reaches opt
            # if not self.reaches_valid:
            #     for i in self.rows:
            #         for
            #     pass
            # return num_letters >= self.reaches_required_length[i][j]
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
        # TODO: make ExpandedSpot data class that tracks letter freshness for scoring purposes
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

    def __str__(self):
        return ' '.join([str(letter) for letter in self.bag])

class Game:
    def __init__(self, board, bag, players):
        self.board = board
        self.bag = bag
        self.players = players
        # TODO: this should really be whover draws the lowest letter from the bag
        self.turn = 0

    def next_player(self):
        self.turn += 1
        return self.players[self.turn % len(self.players)]

    def __str__(self):
        return '{}\nbag: {}\nturn: {}\n{}'.format(
                self.board,
                self.bag,
                self.turn+1,
                '\n'.join(
                    ['{} p{}: {}'.format(
                        '*' if i == (self.turn % len(self.players))
                        else ' ', i, p) for (i, p) in enumerate(self.players)]))

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
    played_letters: Sequence[Letter] = None
    i: int = 0
    j: int = 0
    direction: WordDirection = WordDirection.RIGHT

class Solver:
    def __init__(self, words):
        self.words = words

    def solve(self, board, letters):
        # only deal with letters
        count = 0
        solution = None
        for i in range(ROWS):
            for j in range(COLS):
                permutations = itertools.permutations(letters, len(letters))
                for permutation in permutations:
                    count += 1
                    for l in range(1, len(permutation)):
                        word = permutation[:l]
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
                            for spotted_word in spotted_words:
                                expanded_word = ''.join([spot.letter.letter for spot in spotted_word])
                                all_are_words = all_are_words and expanded_word in self.words
                            score = board.score(spotted_words, i, j, direction)
                            if all_are_words and (solution == None or score > solution.score):
                                solution = Solution(
                                        score = score, word = spotted_words[-1],
                                        played_letters = word, i = i, j = j,
                                        direction = direction)
        pprint.pprint(solution)
        return solution

class Player:
    def __init__(self, board, bag, letters=None, solver=None):
        self.board = board
        self.bag = bag
        self.letters = letters if letters else [bag.draw() for _ in range(7)]
        self.solver = solver

    def take_turn(self):
        solution = self.solver.solve(self.board, self.letters)
        if solution == None:
            return False
        for letter in solution.played_letters:
            self.letters.remove(letter)
            if len(self.bag.bag) > 0:
                self.letters.append(self.bag.draw())
        for spot in solution.word:
            self.board.set_letter(spot.row, spot.col, spot.letter)
        return True

    def __str__(self):
        return ' '.join([str(letter) for letter in self.letters])


def make_game(board_letters=None, bag_letters=None, turn=1, player_letters=[None, None], dictionary='dictionary.txt'):
    spots = [[Spot(i,j) for j in range(0,COLS)] for i in range(0,ROWS)]
    board = Board(spots)
    if board_letters:
        for i, row in enumerate(board_letters.splitlines()):
            for j, letter in enumerate(row.split(' ')):
                board.set_letter(i, j, letter)
    bag = Bag()
    if bag_letters:
        bag.bag = [Letter(letter) for letter in bag_letters.split(' ')]
    word_loader = WordLoader(dictionary)
    solver = Solver(word_loader.words)
    if player_letters != [None, None]:
        player_letters = [[Letter(letter) for letter in player_letter.split(' ')] for player_letter in player_letters]
    players = [Player(board, bag, letters=player_letters[i], solver=solver) for i in range(2)]
    game = Game(board, bag, players)
    game.turn = turn-1
    return game

if __name__ == '__main__':
    game = make_game()
    keep_going = True
    game_start = timeit.default_timer()
    while keep_going:
        turn_start = timeit.default_timer()
        keep_going = game.next_player().take_turn()
        print(game)
        now = timeit.default_timer()
        print('turn time {}s, game time {}s\n\n'.format(now-turn_start, now-game_start), flush=True)
    print('Thanks for playing!')
