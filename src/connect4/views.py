from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import TournamentExecution
from .tournament import get_ai_list

def home(request):

    print("Loading AI Scripts")
    ai_list = get_ai_list("AI_scripts")
    ai_class_names = [ai.__name__ for ai in ai_list] 
    
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

        num_games = int(request.POST.get('num_games',50))

        tournament = TournamentExecution(selected_names, num_games) 
        results = tournament.run_tournament()
        
        context.update({
            'results': results,
            'tournament': tournament,
        })
    
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