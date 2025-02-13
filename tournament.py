import time
from concurrent.futures import ProcessPoolExecutor
from itertools import combinations
from game_engine import RandomPlayer, Game

class Scoreboard:
    def __init__(self, players):
        """Stores results using player names as keys."""
        self.players = {player.name: player for player in players}
        self.results = {player.name: {opponent.name: 0 for opponent in players if opponent != player} for player in players}

    def record_win(self, winner_name, loser_name):
        """Records a win for the winner against the loser in the scoreboard."""
        self.results[winner_name][loser_name] += 1
        
    def display_results(self):
        """Displays the final tournament results."""
        print("\nTournament Results:")
        for player_name in self.results:
            print(f"{player_name}:")
            for opponent_name, wins in self.results[player_name].items():
                print(f"    vs {opponent_name}: {wins} wins")
            print()

def play_match(player1, player2, games_per_match):
    """Plays a set of games between two players and returns the results."""
    local_results = {player1.name: 0, player2.name: 0}

    for _ in range(games_per_match):
        game = Game(player1, player2)
        winner = game.start()
        if winner is not None:
            local_results[winner.name] += 1  # Store wins using player names
    
    return player1.name, player2.name, local_results  # Return names instead of objects

class Tournament:
    def __init__(self, players, games_per_match):
        self.players = players
        self.games_per_match = games_per_match
        self.scoreboard = Scoreboard(players)
        self.total_games = len(list(combinations(players, 2))) * games_per_match

    def run(self):
        """Runs the tournament using parallel processing and measures runtime."""
        matchups = list(combinations(self.players, 2))
        start_time = time.time()  # Start timing execution

        # Use multiprocessing to run games in parallel
        with ProcessPoolExecutor() as executor:
            results = executor.map(play_match, 
                                   [p1 for p1, p2 in matchups], 
                                   [p2 for p1, p2 in matchups], 
                                   [self.games_per_match] * len(matchups))

        # Collect results using names instead of objects
        for player1_name, player2_name, match_results in results:
            for winner_name, wins in match_results.items():
                if wins > 0:
                    loser_name = player1_name if winner_name == player2_name else player2_name
                    for _ in range(wins):
                        self.scoreboard.record_win(winner_name, loser_name)
        
        end_time = time.time()  # End timing execution

        self.scoreboard.display_results()
        self.display_performance_metrics(start_time, end_time)

    def display_performance_metrics(self, start_time, end_time):
        """Calculates and prints tournament performance statistics."""
        total_time = end_time - start_time
        avg_time_per_game = total_time / self.total_games if self.total_games > 0 else 0

        print("\nTournament Performance Metrics:")
        print(f"Total execution time: {total_time:.4f} seconds")
        print(f"Average runtime per game: {avg_time_per_game:.4f} seconds")

if __name__ == '__main__':
    players = [RandomPlayer("A"), RandomPlayer("B"), RandomPlayer("C"), RandomPlayer("D"), RandomPlayer("T")]
    tournament = Tournament(players, games_per_match=1000)
    tournament.run()
