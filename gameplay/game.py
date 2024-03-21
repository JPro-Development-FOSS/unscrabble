COLS = 15
ROWS = COLS

class Letter:
    def __init__(self, letter):
        self.letter = letter

    def __str__(self):
        return '-' if self.letter is None else self.letter


class Spot:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.letter = Letter(None)

class Board:
    def __init__(self, spots):
        self.spots = spots
    
    def __str__(self):
        out = ''
        for row in self.spots:
            out += ' '.join(["{}".format(spot.letter) for spot in row]) + '\n'
        return out

class Bag:
    def __init__(self):
        # TODO
        self.bag = ['a']*100

    def draw(self):
        return self.bag.pop()

class Game:
    def __init__(self, board, bag, players):
        self.board = board
        self.bag = bag
        self.players = players

    def __str__(self):
        return '{}\n{}'.format(
                self.board,
                '\n'.join(['p{}: {}'.format(i, p) for (i, p) in enumerate(self.players)]))

class Player:
    def __init__(self, bag):
        self.bag = bag
        self.letters = [bag.draw() for _ in range(7)]

    def __str__(self):
        return ' '.join(self.letters)
        


spots = [[Spot(i,j) for j in range(0,COLS)] for i in range(0,ROWS)]
board = Board(spots)
bag = Bag()
players = [Player(bag) for _ in range(2)]
game = Game(board, bag, players)
print(game)
