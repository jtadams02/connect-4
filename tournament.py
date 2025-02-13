from concurrent.futures import ProcessPoolExecutor
from itertools import combinations
from game_engine import RandomPlayer, Game

class Scoreboard:
    def __init__(self, players):
        """Initialize the scoreboard with player names instead of objects."""
        self.players = {player.name: player for player in players}  # Map names to player objects
        self.results = {player.name: {opponent.name: 0 for opponent in players if opponent != player} for player in players}

    def record_win(self, winner, loser):
        """Records a win for the winner against the loser using names instead of objects."""
        self.results[winner][loser] += 1
        
    def display_results(self):
        """Displays the final tournament results."""
        print("\nTournament Results:")
        for player, opponents in self.results.items():
            print(f"{player}:")
            for opponent, wins in opponents.items():
                print(f"    vs {opponent}: {wins} wins")
            print()

def play_match(player1, player2, games_per_match):
    """Plays a set of games between two players and returns the results using names."""
    local_results = {player1.name: 0, player2.name: 0}

    for _ in range(games_per_match):
        game = Game(player1, player2)
        winner = game.start()
        if winner is not None:
            local_results[winner.name] += 1  # Store results using player names
    
    return player1.name, player2.name, local_results

class Tournament:
    def __init__(self, players, games_per_match):
        self.players = players
        self.games_per_match = games_per_match
        self.scoreboard = Scoreboard(players)

    def run(self):
        """Runs the tournament using parallel processing."""
        matchups = list(combinations(self.players, 2))

        # Use multiprocessing to run games in parallel
        with ProcessPoolExecutor() as executor:
            results = executor.map(play_match, 
                                   [p1 for p1, p2 in matchups], 
                                   [p2 for p1, p2 in matchups], 
                                   [self.games_per_match] * len(matchups))

        # Collect results
        for player1_name, player2_name, match_results in results:
            for winner_name, wins in match_results.items():
                if wins > 0:
                    loser_name = player1_name if winner_name == player2_name else player2_name
                    for _ in range(wins):
                        self.scoreboard.record_win(winner_name, loser_name)
        
        self.scoreboard.display_results()

if __name__ == '__main__':
    players = [RandomPlayer("A"), RandomPlayer("B"), RandomPlayer("C"), RandomPlayer("D"), RandomPlayer("T")]
    tournament = Tournament(players, games_per_match=1000)
    tournament.run()
