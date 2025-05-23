from django.db import models
from django.contrib.auth.models import User

class UploadFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Connect file to the user
    file_name = models.CharField(max_length=255)
    # file_url = models.URLField()
    # date = models.DateTimeField(auto_now_add=True) # Not sure if this is needed
    visible = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.file_name}"
    
import json

class TournamentExecution:
    def __init__(self, num_players, games_per_match):
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
        players = [random_player(f"Player_{i+1}") for i in range(self.num_players)]
        
        # Run tournament
        tournament = Tournament(players, self.games_per_match)
        tournament.run()
        
        # Calculate win percentage matrix
        player_names = list(tournament.scoreboard.results.keys())
        win_matrix = []
        
        # Create header row
        win_matrix.append([''] + player_names)
        
        # Create data rows
        for player in player_names:
            row = [player]
            for opponent in player_names:
                if player == opponent:
                    row.append('-')
                else:
                    total_matches = (tournament.scoreboard.results[player][opponent] + 
                                   tournament.scoreboard.results[opponent][player])
                    win_rate = (tournament.scoreboard.results[player][opponent] / 
                              total_matches * 100) if total_matches > 0 else 0
                    row.append(f"{win_rate:.1f}%")
            win_matrix.append(row)
        
        # Store results
        # Total games bugs out sometimes, not really sure why. Says 49 occasionally when we set it to 50
        total_games = sum(tournament.scoreboard.total_games.values()) // 2
        total_time = tournament.total_execution_time
        
        self.results = {
            'matrix': tournament.scoreboard.results,
            'win_matrix': win_matrix,
            'total_time': total_time,
            'total_games': total_games,
            'time_per_game': total_time / total_games if total_games > 0 else 0,
            'games_per_second': total_games / total_time if total_time > 0 else 0,
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
    