---
layout: page
title: Documentation
permalink: /docs/
---
<h1 align="center">Connect-4</h1>



## Software Documentation

Welcome to the documentation! This guide will help you install, use, and modify the software, as well as answer common questions.

## Demo Link

Our Demo is currently running at [http://connect-495.com:8000](http://connect-495.com:8000). Feel free to check it out! This demo will only be up for ~3 weeks after 4/25 depending on Google Credits

## Guide Video

[Video Guide Link](https://www.youtube.com/watch?v=jTrQloAHxV4)

## Table of Contents

- [Frequently Asked Questions](#frequently-asked-questions)
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
- [User Guide Video](#uservideo)

---


## Frequently Asked Questions  

### Why isn’t my uploaded AI file showing up on the tournament page?
  Make sure your AI script subclasses the ```DefaultPlayer``` class and implements the required ```get_move()``` function. Also, ensure the file is a valid .py file and does not contain syntax errors. Uploaded files may need to be toggled visible on your profile page.  

### Why are some of my tournament results missing or not saving?

This can happen if a tournament is interrupted or the results exceed memory limits. To prevent data loss, make sure to export your tournament results after completion. Also, ensure the TournamentExecution model in Django is not encountering any errors during save operations.

### Can I run this project without Docker?

Yes! While Docker is supported, it’s not required. You can run the project using Django’s development server. Just activate the virtual environment and run python manage.py runserver from the /src directory as described in the Software Setup section.

### What happens if I run too many games or select too many bots?

Large tournaments with many bots or games can cause performance issues or long runtimes. The backend uses multithreading to help, but the processing power of your machine is still a bottleneck. Consider limiting the number of matchups or using a Dockerized environment for heavy workloads.


## Software Setup

**Download the repository:**

   ```bash
   git clone https://github.com/jtadams02/connect-4.git
   ``` 

**Virtual Enviornment**

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

**Create the Docker image:**

Install Docker, navigate to the /connect4 directory, and execute the following command to create the tournament Docker image:
```console
> docker build -t tournament_image .
```

All dependencies should be installed, to test the server switch to the ```src/``` directory and run the following:
```console
> python manage.py runserver
```

**Google Cloud Information**  
This project uses several aspects of Google Cloud. Our database is hosted on the rather expensive, but convienent CloudSQL service Google provides. The cost can be reduced to about ~$10/month, but that still is expensive.  

Hosting can be done by either CloudRun or Google Compute Engine. CloudRun is the more cost effective option, but not as easy to configure.

Although not fully implemented, using Google Cloud Storage is highly advised for continuation of this project. When deploying using docker, the uploaded files are not always persistent. There exists functionality to use Cloud Storage, but that needs to be enabled in the ```fileupload/views.py``` file.


## User Guide  

### Login System

To login to the Connect-4 website, all you will need is a google account. There is no sign-up option as Django automatically creates a new account for you using the information received by the successful OAUTH call. 

### User Profiles

User Profile pages just hold a history of your uploaded files, and the ability to delete or toggle a file's visibility

### Uploading a Bot:

The menu link titled Upload Agent takes the user to a page where a python file containing an extension of the standard player class. 

### Running A Tournament:

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

# forms.py

Minimal form class for use in views.py . Can be updated but will work as is.


# views.py

This is the main portion of this app that contains most of the logic surronding the file uploads. This is where updates would be made if needed to the file upload systems.

Contains only one function, current version only uploads to media folder

Commented out portion inside function is used for uploading to google cloud. This is functional but will require setting parameters for your own google cloud accounts / deployment.

Currently saving files to directories on the VM. This is an alternative to storing google cloud bucket URLs in a database. 


# urls.py

Sets the url structure for the app.

# media/uploads

Directory in which uploaded media (python connect4 agents) are uploaded and stored in. This is where the VM accesses the uploaded files, but system could be expanded to use the google cloud bucket instead.





