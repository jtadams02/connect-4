from django.shortcuts import render
from .models import TournamentExecution

def home(request):
    if request.method == 'POST':
        num_players = int(request.POST.get('num_players', 2))
        num_games = 50

        # Make sure num_games is not empty
        if request.POST.get('num_games'):
            num_games = int(request.POST.get('num_games',50))

        # Also we're just gonna have the bare minimum be 50 games, cuz we can
        if num_games < 50: num_games=50
        tournament = TournamentExecution(num_players=num_players,games_per_match=num_games) 
        results = tournament.run_tournament()
        return render(request, 'home.html', {
            'results': results,
            'tournament': tournament
        })
    
    return render(request, 'home.html')