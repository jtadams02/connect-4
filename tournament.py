import time
from concurrent.futures import ProcessPoolExecutor
from itertools import combinations
from game_engine import RandomPlayer, Game
import random

class Scoreboard:
    def __init__(self, players):
        """Stores results using player names as keys."""
        self.players = {player.name: player for player in players}
        self.results = {player.name: {opponent.name: 0 for opponent in players if opponent != player} for player in players}
        self.total_wins = {player.name: 0 for player in players}
        self.total_games = {player.name: 0 for player in players}

    def record_win(self, winner_name, loser_name):
        """Records a win for the winner against the loser in the scoreboard."""
        self.results[winner_name][loser_name] += 1
        self.total_wins[winner_name] += 1
        self.total_games[winner_name] += 1
        self.total_games[loser_name] += 1
        
    def display_results(self):
        """Displays the final tournament results."""
        leaderboard = sorted(self.total_wins.items(), key=lambda x: x[1] / self.total_games[x[0]] if self.total_games[x[0]] > 0 else 0, reverse=True)
        
        print("\nLeaderboard:")
        print("----------------------------------")
        print("| Rank | Player | Win Percentage |")
        print("----------------------------------")
        for rank, (player_name, wins) in enumerate(leaderboard, start=1):
            total_win_rate = (wins / self.total_games[player_name] * 100) if self.total_games[player_name] > 0 else 0
            print(f"| {rank:4} | {player_name:10} | {total_win_rate:14.2f}% |")
        print("----------------------------------")
        
        print("\nTournament Results:")
        for player_name in self.results:
            total_win_rate = (self.total_wins[player_name] / self.total_games[player_name] * 100) if self.total_games[player_name] > 0 else 0
            print(f"{player_name} - Overall Win Rate: {total_win_rate:.2f}%")
            for opponent_name, wins in self.results[player_name].items():
                total_matches = self.results[player_name][opponent_name] + self.results[opponent_name][player_name]
                win_rate = (wins / total_matches * 100) if total_matches > 0 else 0
                print(f"    vs {opponent_name}: {wins} wins ({win_rate:.2f}% win rate)")
            print()

def play_match(player1, player2, games_per_match):
    """Plays a set of games between two players and returns the results."""
    local_results = {player1.name: 0, player2.name: 0}
    
    for _ in range(games_per_match):
        if random.choice([True, False]):
            player1, player2 = player2, player1  # Randomize player order
        
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
    print("This is a tournament engine. Each player will play each other a set amount of times.")
    
    # Get the number of players
    num_players = int(input("Enter the number of players: "))
    players = []
    
    for i in range(num_players):
        name = input(f"Enter name for player {i + 1}: ")
        players.append(RandomPlayer(name))
    
    # Get the number of games per matchup
    games_per_match = int(input("Enter the number of games per matchup: "))
    
    # Start tournament
    tournament = Tournament(players, games_per_match)
    tournament.run()
