from django.db import models
from connect4.tournament import Tournament, get_ai_list

class TournamentExecution:
    def __init__(self, player_class_names, games_per_match):
        self.player_class_names = player_class_names
        self.games_per_match = games_per_match
        self.players = self.load_players()
        self.results = None
        self.total_execution_time = None
        
    def load_players(self):
        """Load AI classes based on provided names and instantiate them."""
        available_classes = get_ai_list("AI_scripts")
        class_map = {cls.__name__: cls for cls in available_classes}

        players = []
        for name in self.player_class_names:
            if name in class_map:
                players.append(class_map[name](name))
            else:
                raise ValueError(f"AI class '{name}' not found.")

        return players


    def run_tournament(self):
        """Runs a tournament with the given list of player instances."""
        tournament = Tournament(self.players, self.games_per_match)
        tournament.run()

        player_names = list(tournament.scoreboard.results.keys())
        win_matrix = [[''] + player_names]

        for player in player_names:
            row = [player]
            for opponent in player_names:
                if player == opponent:
                    row.append('-')
                else:
                    total_matches = (
                        tournament.scoreboard.results[player][opponent]
                        + tournament.scoreboard.results[opponent][player]
                    )
                    win_rate = (
                        (tournament.scoreboard.results[player][opponent] / total_matches) * 100
                        if total_matches > 0
                        else 0
                    )
                    row.append(f"{win_rate:.1f}%")
            win_matrix.append(row)

        total_games = sum(tournament.scoreboard.total_games.values()) // 2
        total_time = tournament.total_execution_time

        self.results = {
            'matrix': tournament.scoreboard.results,
            'win_matrix': win_matrix,
            'total_time': total_time,
            'total_games': total_games,
            'time_per_game': total_time / total_games if total_games > 0 else 0,
            'games_per_second': total_games / total_time if total_time > 0 else 0,
            'leaderboard': sorted(
                [
                    {
                        'name': player_name,
                        'wins': wins,
                        'total_games': tournament.scoreboard.total_games[player_name],
                        'win_percentage': (
                            wins / tournament.scoreboard.total_games[player_name] * 100
                            if tournament.scoreboard.total_games[player_name] else 0
                        ),
                    }
                    for player_name, wins in tournament.scoreboard.total_wins.items()
                ],
                key=lambda x: x['win_percentage'],
                reverse=True,
            ),
        }

        self.total_execution_time = total_time
        return self.results
