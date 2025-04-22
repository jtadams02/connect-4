from django.db import models
import subprocess
import json
import os

#executes the given tournament
class TournamentExecution:
    def __init__(self, player_class_names, games_per_match):
        self.player_class_names = player_class_names
        self.games_per_match = games_per_match
        self.results = None
        self.total_execution_time = None

    def run_tournament(self):
        """Runs a containerized tournament with the given list of player names."""

        cmd = [
            'docker', 
            'run', 
            '--rm', 
            '-v', 
            f'{os.getcwd()}/connect4/AI_scripts:/app/connect4/AI_scripts', 
            'tournament_image', 
            'python', 
            '-m', 
            'connect4.tournament', 
        ] + self.player_class_names + [str(self.games_per_match)]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        tournament_data = json.loads(result.stdout)

        results = tournament_data['scoreboard']['results']
        total_games = tournament_data['scoreboard']['total_games']
        total_wins = tournament_data['scoreboard']['total_wins']
        total_time = tournament_data['total_execution_time']

        player_names = list(results.keys())
        win_matrix = [[''] + player_names]

        for player in player_names:
            row = [player]
            for opponent in player_names:
                if player == opponent:
                    row.append('-')
                else:
                    total_matches = (
                        results[player][opponent] +
                        results[opponent][player]
                    )
                    win_rate = (
                        (results[player][opponent] / total_matches) * 100
                        if total_matches > 0 else 0
                    )
                    row.append(f"{win_rate:.1f}%")
            win_matrix.append(row)

        game_count = sum(total_games.values()) // 2

        self.results = {
            'matrix': results,
            'win_matrix': win_matrix,
            'total_time': total_time,
            'total_games': game_count,
            'time_per_game': total_time / game_count if game_count > 0 else 0,
            'games_per_second': game_count / total_time if total_time > 0 else 0,
            'leaderboard': sorted(
                [
                    {
                        'name': player_name,
                        'wins': wins,
                        'total_games': total_games[player_name],
                        'win_percentage': (
                            wins / total_games[player_name] * 100
                            if total_games[player_name] else 0
                        )
                    }
                    for player_name, wins in total_wins.items()
                ],
                key=lambda x: x['win_percentage'],
                reverse=True
            )
        }

        self.total_execution_time = total_time
        return self.results

if __name__ == '__main__':
    import sys
    args = sys.argv
    player_class_names = args[1:-1]
    games_per_match = int(args[-1])
    TE = TournamentExecution(player_class_names, games_per_match)
    print(TE.run_tournament())