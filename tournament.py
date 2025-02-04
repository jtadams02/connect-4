import random
from itertools import combinations
from game_engine import RandomPlayer, Game
#Has built in function to return cross product

class Tournament:
    def __init__(self, players, games_per_match):
        self.players = players
        self.games_per_match = games_per_match

    def run(self):
        #Runs the tournament
        matchups = list(combinations(self.players, 2))

        for _ in range(self.games_per_match):
            for player1, player2 in matchups:
                game = Game(player1, player2)
                winner = game.start()
                print(f"{player1} vs {player2} winner: {winner}")

if __name__ == '__main__':
    players = [RandomPlayer("A"), RandomPlayer("B"), RandomPlayer("C"), RandomPlayer("D"), RandomPlayer("T")]
    tournament = Tournament(players, games_per_match=3)
    tournament.run()