from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import TournamentExecution
from .tournament import get_ai_list
from django.http import HttpResponse
import json
from datetime import datetime


def home(request):
    print("Loading AI Scripts")
    ai_list = get_ai_list("connect4/AI_scripts")  # import ai list from directory
    ai_class_names = [ai.__name__ for ai in ai_list]  # extract just the names from the list
    print("Available AI Scripts: ", ai_class_names)

    context = {
        'ai_class_names': ai_class_names,
        'results': None,
        'error': None,
    }

    if request.method == 'POST':
        # Check if importing a JSON file
        if 'import_json' in request.POST:
            uploaded_file = request.FILES.get('json_file')
            if uploaded_file:
                try:
                    # Load the JSON data from the uploaded file
                    data = json.load(uploaded_file)
                    # Validate structure by checking the keys
                    if all(key in data for key in ['total_games', 'total_time', 'time_per_game', 'games_per_second', 'leaderboard', 'win_matrix']):
                        request.session['tournament_results'] = data
                        context['results'] = data
                        print("Successfully imported tournament results.")
                    else:
                        context['error'] = "Invalid JSON data format."
                except json.JSONDecodeError:
                    context['error'] = "Invalid JSON file format."
            else:
                context['error'] = "No file selected for import."
            return render(request, 'home.html', context)

        # Clear previous tournament results if they exist
        if 'tournament_results' in request.session:
            print("Clearing previous tournament results from session")
            del request.session['tournament_results']

        # Run a new tournament
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

        # Store results in session
        request.session['tournament_results'] = results
        context['results'] = results
        return redirect('home')

    elif 'tournament_results' in request.session:
        context['results'] = request.session.get('tournament_results')

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
    
def export_results(request):
    results = request.session.get('tournament_results', None)
    if results is None:
        return HttpResponse("No Tournament results to export.", status=404)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{current_time}_tournament_results.json"
    response = HttpResponse(json.dumps(results, indent=4), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response
