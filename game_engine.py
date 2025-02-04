import random as rn

class Board():
    '''
        Stores a Connect4 board state. Moves may be applies, and winners/draws are returned.
        The 2D board array is indexed by board[column][row] where columns start from the left and rows start from the bottom.
    '''
    char_map = {0: ".", -1: "o", 1: "x"}
    win_dirs = [(0,1), (1,0), (1,1), (1,-1)]

    def __init__(self):
        self.board = [[0]*6 for i in range(7)]

    def __repr__(self):
        s = ""
        for row in range(5,-1,-1):
            for col in range(7):
                s = s + self.char_map[self.board[col][row]]
            s = s + "\n"
        return s[:-1]
    
    def is_valid_move(self, col:int):
        return not self.board[col][-1]
    
    def get_valid_moves(self):
        return [col for col in range(7) if self.is_valid_move(col)]
    
    def check_win_dir(self, d_col:int, d_row:int):
        mn_row = 3 if d_row == -1 else 0
        mx_row = 3 if d_row == 1 else 6
        mn_col = 3 if d_col == -1 else 0
        mx_col = 4 if d_col == 1 else 7
        for col in range(mn_col, mx_col):
            for row in range(mn_row, mx_row):
                val = self.board[col][row]
                if val and len(set(self.board[col+i*d_col][row+i*d_row] for i in range(4))) == 1:
                    return val
        return None
    
    def check_win(self):
        if not self.get_valid_moves():
            return 0
        for dir in self.win_dirs:
            dir_win = self.check_win_dir(*dir)
            if dir_win is not None:
                return dir_win
        return None

    def move(self, turn:int, col:int):
        assert self.is_valid_move(col), f"Invalid move: column {col} is full."
        col_ind = self.board[col].index(0)
        self.board[col][col_ind] = turn
        return self.check_win()
    
class Player():
    '''
        Player class which has a name a method to make a move given a Connect4 board (default is the first available move).
    '''
    def __init__(self, name:str):
        self.name = name

    def __repr__(self):
        return self.name

    def get_move(self, board:Board):
        return board.get_valid_moves()[0]

class RandomPlayer(Player):
    '''
        Player subclass that makes random moves.
    '''
    def get_move(self, board:Board):
        return rn.choice(board.get_valid_moves())

class Game():
    '''
        Game class which takes in two player and runs a game between them once start() is envoked.
    '''
    def __init__(self, player1:Player, player2:Player):
        self.players = {1: player1, -1: player2}
        self.c4board = Board()
        self.moves = []
        self.winner = 0

    def print_move(self, turn:int, move:int):
        print("".join(Board.char_map[turn] if col==move else " " for col in range(7)))
        print("".join("|" if col==move else "-" for col in range(7)))
        print(f"{self.c4board}\n")

    def start(self, first:int=1, verbose:bool=False):
        CM = Board.char_map
        if verbose:
            print(f"\nPlayer 1: {self.players[first].name} - {CM[first]},  Player 2: {self.players[-first].name} - {CM[-first]}.\n")
        turn = first
        while 1:
            move = self.players[turn].get_move(self.c4board)
            win = self.c4board.move(turn, move)
            self.moves.append(move)
            if verbose:
                self.print_move(turn, move)
            if win is not None:
                self.winner = win
                break
            turn *= -1
        if verbose:
            if self.winner:
                print(f"Player {self.players[self.winner].name} wins.")
            else:
                print("draw.")
        return self.players[self.winner]
    
if __name__ == "__main__":
    import random as rn

    a1 = RandomPlayer("A")
    a2 = RandomPlayer("B")

    first = 1
    while 1:
        game = Game(a1, a2)
        game.start(first=first, verbose=True)
        if input('-'*20):
            break
        print('Starting new game.\n')
        first *= -1