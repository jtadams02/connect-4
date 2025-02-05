import random
from itertools import combinations
from game_engine import RandomPlayer, Game
#Has built in function to return cross product

class Scoreboard:
    def __init__(self, players):
        self.players = players
        self.results = {player: {opponent: 0 for opponent in players if opponent != player} for player in players}

    # Update tournament scoreboard
    def record_win(self, winner, loser):
        self.results[winner][loser] += 1
        
    #display tournament scoreboard
    def display_results(self):
        print("\nTournament Results:")
        for player in self.players:
            print(f"{player}:")
            for opponent, wins in self.results[player].items():
                print(f"    vs {opponent}: {wins} wins")
            print()


class Tournament:
    def __init__(self, players, games_per_match):
        self.players = players
        self.games_per_match = games_per_match
        self.scoreboard = Scoreboard(players)

    def run(self):
        #Runs the tournament
        matchups = list(combinations(self.players, 2))

        for _ in range(self.games_per_match):
            for player1, player2 in matchups:
                game = Game(player1, player2)
                winner = game.start()
                sufix = "tie" if winner is None else f"{winner} wins"
                print(f"{player1} vs {player2}: {sufix}")
                if winner is not None:
                    loser = player1 if winner == player2 else player2
                    self.scoreboard.record_win(winner, loser)
    
        self.scoreboard.display_results()

if __name__ == '__main__':
    players = [RandomPlayer("A"), RandomPlayer("B"), RandomPlayer("C"), RandomPlayer("D"), RandomPlayer("T")]
    tournament = Tournament(players, games_per_match=3)
    tournament.run()