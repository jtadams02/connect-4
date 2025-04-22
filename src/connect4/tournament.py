import time
import importlib.util
import os
import sys
import json
import inspect
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from connect4.game_engine import Game

#class to store and display tournament results 
class Scoreboard:
    def __init__(self, players):
        """Stores results using player names as keys."""
        self.results = {player.name: {opponent.name: 0 for opponent in players if opponent != player} for player in players}
        self.total_wins = {player.name: 0 for player in players}
        self.total_games = {player.name: 0 for player in players}

    def to_dict(self):
        return {
            'results': self.results, 
            'total_wins': self.total_wins,
            'total_games': self.total_games
        }

    def record_win(self, winner_name, loser_name):
        """Records a win for the winner against the loser in the scoreboard."""
        self.results[winner_name][loser_name] += 1
        self.total_wins[winner_name] += 1
        self.total_games[winner_name] += 1
        self.total_games[loser_name] += 1
        
    def display_results(self):
        """Displays the final tournament results."""
        leaderboard = sorted(self.total_wins.items(), key=lambda x: x[1] / self.total_games[x[0]] if self.total_games[x[0]] > 0 else 0, reverse=True)
        
        line_str = "-"*34
        print("\nLeaderboard:")
        print(line_str)
        print("| Rank |   Player   |   Win %   |")
        print(line_str)
        for rank, (player_name, wins) in enumerate(leaderboard, start=1):
            total_win_rate = (wins / self.total_games[player_name] * 100) if self.total_games[player_name] > 0 else 0
            print(f"| {rank:4} | {player_name:10} | {total_win_rate:8.2f}% |")
        print(line_str)
        
        #displays a matrix of the results for each matchup
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

#class for tournament, holding players and executing games
class Tournament:
    def __init__(self, player_class_names, games_per_match):
        self.player_class_names = player_class_names
        self.players = self.load_players()
        self.games_per_match = games_per_match
        self.scoreboard = Scoreboard(self.players)
        self.total_games = ((len(self.players)*(len(self.players)-1))//2) * games_per_match
        self.total_execution_time = None

    def to_dict(self):
        return {
            'player_class_names': self.player_class_names, 
            'games_per_match': self.games_per_match,
            'scoreboard': self.scoreboard.to_dict(),
            'total_games': self.total_games,
            'total_execution_time': self.total_execution_time
        }
    
    def serialize(self):
        return json.dumps(self.to_dict())

    def load_players(self):
        """Load AI classes based on provided names and instantiate them."""
        available_classes = get_ai_list("connect4/AI_scripts") #import ais, cannot directly pass from the import in views.py
        class_map = {cls.__name__: cls for cls in available_classes}

        players = []
        for name in self.player_class_names:
            if name in class_map:
                players.append(class_map[name](name))
            else:
                raise ValueError(f"AI class '{name}' not found.")

        return players

    def run(self, verbose=True):
        """Runs the tournament using parallel processing and measures runtime."""
        matchups = list(combinations(self.players, 2)) #creates all matchups, in round robin format with each player playing every other player 
        start_time = time.time()  # Start timing execution

        # Use multiprocessing to run games in parallel to increase performance
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
        self.total_execution_time = end_time - start_time

        if verbose:
            self.scoreboard.display_results() #display results
            self.display_performance_metrics(start_time, end_time) #display time metrics

    def display_performance_metrics(self, start_time, end_time):
        """Calculates and prints tournament performance statistics."""
        total_time = end_time - start_time
        avg_time_per_game = total_time / self.total_games if self.total_games > 0 else 0

        print("\nTournament Performance Metrics:")
        print(f"Total execution time: {total_time:.4f} seconds")
        print(f"Average runtime per game: {avg_time_per_game:.4f} seconds")

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

def get_ai_list(dir):
    """Import all AI classes present in a given directory."""
    ai_files = [file for file in os.listdir(dir) if file.endswith(".py")]
    assert "DefaultPlayer.py" in ai_files, "DefaultPlayer.py not found in AI_Scripts." #manually ensures the default player template is loaded first
    ai_files.remove("DefaultPlayer.py")
    ai_files.insert(0, "DefaultPlayer.py")

    ai_list = []
    for file in ai_files:
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

if __name__ == '__main__':
    args = sys.argv
    player_class_names = args[1:-1]
    games_per_match = int(args[-1])
    tournament = Tournament(player_class_names, games_per_match)
    tournament.run(verbose=False)
    print(tournament.serialize())