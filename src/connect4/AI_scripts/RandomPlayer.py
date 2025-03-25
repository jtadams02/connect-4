#from DefaultPlayer import DefaultPlayer
import random as rn
class DefaultPlayer():
    '''
        Player class which has a name a method to make a move given a Connect4 board (default is the first available move).
    '''
    def __init__(self, name:str):
        self.name = name

    def __repr__(self):
        return self.name

    def get_move(self, board, turn):
        return board.get_valid_moves()[0]
class RandomPlayer(DefaultPlayer):
    '''
        Player subclass that makes random moves.
    '''
    def get_move(self, board, turn):
        return rn.choice(board.get_valid_moves())