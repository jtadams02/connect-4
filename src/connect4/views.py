from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import TournamentExecution
from .tournament import get_ai_list


def home(request):
    print("Loading AI Scripts")
    ai_list = get_ai_list("connect4/AI_scripts")
    ai_class_names = [ai.__name__ for ai in ai_list] 
    print("Available AI Scripts: ", ai_class_names)
    
    context = {
        'ai_class_names': ai_class_names,
        'results': None,
    }

    if request.method == 'POST':
        selected_names = request.POST.getlist('selected_ais')

        if not selected_names:
            context['error'] = "No AI classes selected."
            return render(request, 'home.html', context)

        print(f"Selected AI classes from POST: {selected_names}")

        num_games = int(request.POST.get('num_games', 50))
        print("Games per Matchup: ", num_games)
        print("Running tournament")
        tournament = TournamentExecution(selected_names, num_games)
        results = tournament.run_tournament()

        # Serialize results and store in session
        request.session['tournament_results'] = results  # Make sure `results` is JSON-serializable
        return redirect('home')  # Redirect to avoid re-POST on refresh

    elif 'tournament_results' in request.session:
        context['results'] = request.session.pop('tournament_results')  # Use and remove it

    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # Why is this request.POST?
        if form.is_valid():
            form.save() # Save new user to DB
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request,"register.html", {
        "form" : form,
    })