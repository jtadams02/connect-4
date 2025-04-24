<h1 align="center">Connect-4</h1>

## Table of Contents

- [Software Setup](#software-setup)
- [User Guide](#user-guide)
  - [Login System](#login-system)
  - [User Profiles](#user-profiles)
  - [Uploading a Bot](#uploading-a-bot)
  - [Running a Tournament](#running-a-tournament)
- [Code Overview](#code-overview)
  - [game_engine.py](#game_enginepy)
  - [tournament.py](#tournamentpy)
  - [DefaultPlayer.py](#defaultplayerpy)
  - [models.py](#modelspy)
  - [views.py](#viewspy)
- [File Upload](#file-upload)

---


## Software Setup

**Virtual Environment** 

First setup the virtual environment by going into the root directory, and running the following 
```console
> py -3.13 -m venv .env
```
*(You may need to install the lastest version of python, ensure to install it to path)*

 Once the env is generated, you need to activate it, to do so on Windows use the following command:
 ```console
> .env\Scripts\activate.bat
```

Now the virtualenv is activated, install the requirements using this:
```console
> pip install -r requirements.txt
```

All dependencies should be installed, to test the server switch to the ```src/``` directory and run the following:
```console
> python manage.py runserver
```

**Creating the Docker image:**

Install Docker, navigate to the /connect4 directory, and execute the following command to create the tournament Docker image:
```console
> docker build -t tournament_image .
```

All dependencies should be installed, to test the server switch to the ```src/``` directory and run the following:
```console
> python manage.py runserver
```

## User Guide

**Login System**

To login to the Connect-4 website, all you will need is a google account. There is no sign-up option as Django automatically creates a new account for you using the information received by the successful OAUTH call. 

**User Profiles**

User Profile pages just hold a history of your uploaded files, and the ability to delete or toggle a file's visibility

**Uploading a Bot**

The menu link titled Upload Agent takes the user to a page where a python file containing an extension of the standard player class. 

**Running A Tournament**

First select which AI Agents are to be included in the tournament
This tournament will be a round robin format tournament, so each chosen model will compete against every other model.

Select the number of games for each matchup. This rapidly scales with the total number of models selected. The Run Tournament button will execute a tournament with the chosen parameters

If instead the user wishes to import the results of a previous tournament the appropriate JSON file can be uploaded and imported. This will display the results of the past tournament to the user.

After a tournament has been executed its results will be shown. First there is the statistics for the tournament itself such as the total number of games played and the time data for it.

The section titled leaderboard displays the players ranked according to overall win percentage. 

The section titled Win Percentae Matrix displays the players individualized win percentages for each matchup.

At the bottom of the page there is an option to export the results of a tournament. This will be a JSON containing the displayed information that can later be uploaded to view these results.

## Code Overview
### game_engine.py

This is the Connect-4 Engine used by the application.

### tournament.py

This file contains the tournament engine. It executes a round robin format tournament using the game_engine.py. It consists of two classes, Scoreboard and Tournament, and two helper functions.

The Scoreboard class stores the players, game results, and contains a function for displaying the full results of an executed tournament. It accepts a list of players as a parameter and is used by the Tournament class.

The Tournament class accepts a list of player_class_names strings and integer of games_per_match. It loads the players using the get_ai_list function. It then executes the tournament in the run function using python's ThreadPoolExecutor to run the games in parallel. It also tracks and displays time metrics.

The play_match function executes a set number of games between two players. It swaps which player is player1 and player2 each game, this is to prevent the tournament from being biased as the first player has a small advantage in Connect 4.

The get_ai_list function accepts a directory as a parameter and imports a list of all python files as imported modules found in the given directory.

### DefaultPlayer.py

This file, stored in the AI_Scripts folder, is the default player class that all agents are subclasses of. These agents pass moves using the get_move function

### models.py

This contains the django model to run a tournament, stored in the class TournamentExecution. It accepts a list of player_class_names strings and integer of games_per_match. It creates a container in which a tournament is run using these parameters. It then stores the results of the tournament in its results variable.

### views.py

This consists of three possible views; home, register, and export_results.

Home is the primary view for tournament execution. It first loads and displays the list of available ai agents. It calls get_ai_list but discards the imported list of ai modules, only using the names from this call. This is a mild performance inefficiency, however passing imported agents as modules was not functioning correctly so instead calling get_ai_list twice was used.

Upon recieving a POST request it first checks if the user is running a tournament or importing a JSON file of a previous tournament's results. If importing, it displays the recieved data. Otherwise, it executes a tournament using the selected AI Agents.

The Register view is used to allow the user to register a new account.

The export_results view exports the currently displayed tournament results, if it exists. It uses the current exact date to the second as the name of the JSON to ensure unique and useful naming.

### fileupload

The file uploading features of this application were developed as a seperate app in Django, so it has it's own views.py, urls.py, etc. 

Please see the README in the file upload sub-directory to learn more