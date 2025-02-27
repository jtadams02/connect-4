import time
import importlib.util
import os
import sys
import inspect
import json
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from game_engine import Game

RESULTS_FILE = "central_results.json"
GAMES_PER_MATCH = 100 #hardcoded gpm

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
        
    def save_results(self):
        """Saves the results to a JSON file in 'past_tournaments'"""
        folder = os.path.abspath("past_tournaments") 
        os.makedirs(folder, exist_ok=True)  # Create if it doesn't exist
        
        filename = os.path.join(folder, f"results_{int(time.time())}.json")
        
        leaderboard = sorted(self.total_wins.items(), key=lambda x: x[1] / self.total_games[x[0]] if self.total_games[x[0]] > 0 else 0, reverse=True)
        
        # Prepare leaderboard data
        leaderboard_data = [
            {"rank": rank + 1, "player": player_name, "win_percentage": (wins / self.total_games[player_name] * 100) if self.total_games[player_name] > 0 else 0}
            for rank, (player_name, wins) in enumerate(leaderboard)
        ]

        # Prepare win percentage matrix
        win_matrix = {}
        for player in self.results:
            win_matrix[player] = {}
            for opponent in self.results[player]:
                total_matches = self.results[player][opponent] + self.results[opponent][player]
                win_rate = (self.results[player][opponent] / total_matches * 100) if total_matches > 0 else 0
                win_matrix[player][opponent] = win_rate

        # Save to JSON
        with open(filename, "w") as f:
            json.dump({"leaderboard": leaderboard_data, "win_matrix": win_matrix}, f, indent=4)

        print(f"\nTournament results saved to {filename}")
        
    def display_results(self):
        """Displays the final tournament results."""
        leaderboard = sorted(self.total_wins.items(), key=lambda x: x[1] / self.total_games[x[0]] if self.total_games[x[0]] > 0 else 0, reverse=True)
        
        line_str = "-"*33
        print("\nLeaderboard:")
        print(line_str)
        print("| Rank |   Player   |   Win %   |")
        print(line_str)
        for rank, (player_name, wins) in enumerate(leaderboard, start=1):
            total_win_rate = (wins / self.total_games[player_name] * 100) if self.total_games[player_name] > 0 else 0
            print(f"| {rank:4} | {player_name:10} | {total_win_rate:8.2f}% |")
        print(line_str)
        
        print("\nWin Percentage Matrix:")
        player_names = list(self.results.keys())
        header = "        " + "  ".join(f"{name[:5]:>5}" for name in player_names)
        print(header)
        print("  " + "-" * len(header))
        for player in player_names:
            row = [f"{player[:5]:>5}"]
            for opponent in player_names:
                if player == opponent:
                    row.append("  -  ")  # No self-matches
                else:
                    total_matches = self.results[player][opponent] + self.results[opponent][player]
                    win_rate = (self.results[player][opponent] / total_matches * 100) if total_matches > 0 else 0
                    row.append(f"{win_rate:5.1f}%")
            print("  ".join(row))
            
        self.save_results() #saves the results to json

def play_match(player1, player2, games_per_match):
    """Plays a set of games between two players and returns the results."""
    local_results = {player1.name: 0, player2.name: 0}
    
    for _ in range(games_per_match):
        player1, player2 = player2, player1  # Swap player order
        
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
        with ThreadPoolExecutor() as executor:
            p1_list, p2_list = zip(*matchups)
            results = executor.map(play_match, p1_list, p2_list, [self.games_per_match] * len(matchups))

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

def get_ai_list(dir):
    """Import all AI classes present in a given directory."""
    ai_list = []
    for file in os.listdir(dir):
        if file.endswith(".py"):
            module_name = file[:-3]
            module_path = os.path.join(dir, file)
            
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__name__ == module_name:
                    ai_list.append(obj)
                    break
    
    return ai_list

def get_ai_classes(directory):
    ai_classes = []
    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]  # Remove .py extension
            module_path = os.path.join(directory, filename)

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find all classes in the module
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type):  # Check if it's a class
                    ai_classes.append(attr)
    
    return ai_classes

if __name__ == '__main__':
    print("\nThis is a tournament engine. This version will keep a persistent record of all AIs in AI_scripts against each other.")

    # Get all AI player classes from the AI_scripts directory
    AI_list = get_ai_classes("AI_scripts")

    # Create players from each AI class
    players = [ai_class(f"Player {i+1}") for i, ai_class in enumerate(AI_list)]

    # Get the number of games per matchup
    games_per_match = GAMES_PER_MATCH
        
    # Start tournament
    tournament = Tournament(players, games_per_match)
    tournament.run()