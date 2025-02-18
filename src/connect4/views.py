from django.shortcuts import render
from .models import TournamentExecution

def home(request):
    if request.method == 'POST':
        num_players = int(request.POST.get('num_players', 2))
        tournament = TournamentExecution(num_players=num_players)
        results = tournament.run_tournament()
        return render(request, 'home.html', {
            'results': results,
            'tournament': tournament
        })
    
    return render(request, 'home.html')