import cProfile
import game

if __name__ == '__main__':
    board='''- - - - - - - - - - - - - - -
- - - - - - - - - - - - - - -
- - - - - - - - - - - - - - -
- - - - - - - - - - - - - - -
- - - - - - - G - - - - - - -
- - - - - - - R - - - - - - -
- - - - - - F E H - - - - - -
- - - - - - A Y E - D - - - -
- - - - - - E - N A E - - - -
- - - - - - C - S I C - - - -
- - - - - - A G - - A A - - -
- - - - - - L I - - F A - - -
- - - - - - - T - - - - - - -
- - - - - - - - - - - - - - -
- - - - - - - - - - - - - - -'''
    bag='N N H B U B W W S L S A R U M P A J T N T O R E E I O Z P T E E U V D R I Q A D U O M T E X E O V O R I O N E L _ G R N'
    player_letters=['O I Y D S T K', '_ I I I O E L']
    cProfile.run(
            f'''g=game.make_game(board_letters=\'\'\'{board}\'\'\',bag_letters='{bag}',turn=8,player_letters={player_letters}); g.next_player().take_turn(); print(g)''')
