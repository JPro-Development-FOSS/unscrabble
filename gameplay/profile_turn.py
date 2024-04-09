import cProfile
import game

if __name__ == '__main__':
    cProfile.run('game.make_game().players[0].take_turn()')
