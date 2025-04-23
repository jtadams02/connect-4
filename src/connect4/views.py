from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from .models import TournamentExecution
from .tournament import get_ai_list
from django.http import HttpResponse
import json
from datetime import datetime

from fileupload.models import UploadFile

# Get OAUTH view
from allauth.socialaccount.providers.google.views import OAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client



def home(request):
    # Make website inaccessible to non-logged in users!
    if not request.user.is_authenticated:
        return render(request, 'home_guest.html')
    
    print("Loading AI Scripts")
    ai_list = get_ai_list("connect4/AI_scripts")  # import ai list from directory.
    #^^^ This is not actually imported into the tournament call later, it was causing problems so saving just the names and passing that was a workaround. This has some performance implications but probably acceptable
    get_visible_files  = UploadFile.objects.filter(visible=True)
    visible_files = [res.file_name[:-3] for res in get_visible_files]
    print(visible_files)
    # Now add the base classes to the visible list:
    visible_files.append("RandomPlayer")
    visible_files.append("MiniMaxPlayer")
    visible_files.append("DefaultPlayer")
    visible_files.append("ExamplePlayer ")
    print(ai_list)
    # Need to only show toggled AI Scripts
    ai_class_names = [ai.__name__ for ai in ai_list if ai.__name__ in visible_files]  # extract just the names from the list
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


def user_profile(request):
    user_files = UploadFile.objects.filter(user=request.user)
    return render(request, 'profile.html', {'user_files': user_files})

def toggle_visibility(request, file_id):
    currently_visible_file = UploadFile.objects.filter(user=request.user,visible=True).first()

    # If there are no visible files right now, just toggle the one the user requested
    if currently_visible_file is None:
        file = get_object_or_404(UploadFile, id=file_id, user=request.user)
        file.visible = not file.visible
        file.save()
        return redirect('user_profile')
    
    # if the user is trying to toggle the currently visible file, just toggle it off
    if (file_id == currently_visible_file.id):
        currently_visible_file.visible = not currently_visible_file.visible
        currently_visible_file.save()
        return redirect('user_profile')
    else: 
        # If there is already a visible file, print an error message!
        e = "You can only have one visible file at a time!"
        return redirect('user_profile')
def delete_file(request, file_id):
    file = get_object_or_404(UploadFile, id=file_id, user=request.user)
    file.delete()
    return redirect('user_profile')

def oauth_login(request):
    # Redirect to Google OAuth login
    return redirect("/accounts/google/login/?next=/")
