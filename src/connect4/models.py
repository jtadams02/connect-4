from django.db import models
import json

class TournamentExecution:
    def __init__(self, num_players, games_per_match=10):
        self.num_players = num_players
        self.games_per_match = games_per_match
        self.results = None
        self.total_execution_time = None

    def run_tournament(self):
        """Runs a tournament with the specified number of players using RandomPlayer"""
        from connect4.tournament import Tournament, get_ai_list
        
        # Get the RandomPlayer class
        ai_classes = get_ai_list("AI_scripts")
        random_player = next(cls for cls in ai_classes if cls.__name__ == "RandomPlayer")
        
        # Create player instances
        players = [
            random_player(f"Player_{i+1}")
            for i in range(self.num_players)
        ]
        
        # Run tournament
        tournament = Tournament(players, self.games_per_match)
        tournament.run()
        
        # Store results
        self.results = {
            'matrix': tournament.scoreboard.results,
            'leaderboard': [
                {
                    'name': player_name,
                    'wins': wins,
                    'total_games': tournament.scoreboard.total_games[player_name],
                    'win_percentage': (wins / tournament.scoreboard.total_games[player_name] * 100)
                }
                for player_name, wins in sorted(
                    tournament.scoreboard.total_wins.items(),
                    key=lambda x: x[1] / tournament.scoreboard.total_games[x[0]],
                    reverse=True
                )
            ]
        }
        
        self.total_execution_time = tournament.total_execution_time
        return self.results