from DefaultPlayer import DefaultPlayer
import random as rn

class RandomPlayer(DefaultPlayer):
    '''
        Player subclass that makes random moves.
    '''
    def get_move(self, board):
        return rn.choice(board.get_valid_moves())