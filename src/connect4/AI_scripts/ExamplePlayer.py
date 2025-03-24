from DefaultPlayer import DefaultPlayer
import math
#this is just MiniMaxPlayer but with a deeper MiniMax depth

class ExamplePlayer(DefaultPlayer):
    val_map = {1: 1, 2: 4, 3: 20}

    def get_move(self, board, turn):
        return self.minimax(board, 3, -math.inf, math.inf, turn)[0]
    
    def minimax(self, board, depth, alpha, beta, turn):
        valid_moves = board.get_valid_moves()
        
        w = board.check_win()
        if w in [-1,1]:
            val = w*((depth+1)*1e9)
            return None, val

        if depth == 0 or not valid_moves:
            val = self.eval_board(board)
            return None, val

        if turn == 1:
            max_eval = -math.inf
            max_move = None
            for move in valid_moves:
                new_board = board.copy()
                new_board.move(1, move)
                _, eval = self.minimax(new_board, depth - 1, alpha, beta, -1)
                if eval > max_eval:
                    max_eval = eval
                    max_move = move
                if max_eval > beta:
                    break
                alpha = max(alpha, max_eval)
            return max_move, max_eval
        else:
            min_eval = math.inf
            min_move = None
            for move in valid_moves:
                new_board = board.copy()
                new_board.move(-1, move)
                _, eval = self.minimax(new_board, depth - 1, alpha, beta, 1)
                if eval < min_eval:
                    min_eval = eval
                    min_move = move
                if min_eval < alpha:
                    break
                beta = min(beta, min_eval)
            return min_move, min_eval
        
    def eval_block(self, L):
        if set(L) == {0, 1}:
            return self.val_map[L.count(1)]
        elif set(L) == {0, -1}:
            return -self.val_map[L.count(-1)]
        return 0
        
    def eval_board(self, board):
        val = 0
        for col in range(7):
            for ri in range(3):
                L = board.board[col][ri:ri+4]
                val += self.eval_block(L)
        for row in range(6):
            for ci in range(4):
                L = [board.board[ci+i][row] for i in range(4)]
                val += self.eval_block(L)
        for ci in range(4):
            for ri in range(3):
                L = [board.board[ci+i][ri+i] for i in range(4)]
                val += self.eval_block(L)
                L = [board.board[ci+i][5-ri-i] for i in range(4)]
                val += self.eval_block(L)

        return val