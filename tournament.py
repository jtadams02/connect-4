import random
from itertools import combinations
#Has built in function to return cross product

class Player:
    def __init__(self, name):
        self.name = name
        self.wins = 0

    def __str__(self):
        return self.name
    
    def inc(self):
        self.wins += 1
        
    def score(self):
        return self.wins
    
class Scoreboard:
    def __init__ (self, players):
        self.players = players
                    
    def out(self):
        for player in players:
            print(f"Player {player.__str__()} score: {player.score()}")

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def play(self):
        #Simulates a game
        winner = random.choice([self.player1, self.player2])
        return winner

class Tournament:
    def __init__(self, players, games_per_match):
        self.players = players
        self.games_per_match = games_per_match

    def run(self):
        #Runs the tournament
        matchups = list(combinations(self.players, 2))

        for _ in range(self.games_per_match):
            for player1, player2 in matchups:
                game = Game(player1, player2)
                winner = game.play()
                winner.inc()
                print(f"{player1} vs {player2} winner: {winner}")

players = [Player("A"), Player("B"), Player("C"), Player("D"), Player("T")]
tournament = Tournament(players, games_per_match=100)
tournament.run()
scoreboard = Scoreboard(players)
scoreboard.out()