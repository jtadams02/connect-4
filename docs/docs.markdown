---
layout: page
title: Documentation
permalink: /docs/
---


# Software Documentation

Welcome to the documentation! This guide will help you install, use, and modify the software, as well as answer common questions.

---

## How to Install Software

**Download the repository:**
   ```bash
   git clone https://github.com/jtadams02/connect-4.git

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

All dependencies should be installed, to test the server switch to the ```src/``` directory and run the following:
```console
> python manage.py runserver
```


# How To Use Each Feature

Login System

To-Do

User Profiles

To-Do

Uploading a Bot

The menu link titled Upload Agent takes the user to a page where a python file containing an extension of the standard player class. 

Running A Tournament

First select which AI Agents are to be included in the tournament
This tournament will be a round robin format tournament, so each chosen model will compete against every other model.

Select the number of games for each matchup. This rapidly scales with the total number of models selected. The Run Tournament button will execute a tournament with the chosen parameters

If instead the user wishes to import the results of a previous tournament the appropriate JSON file can be uploaded and imported. This will display the results of the past tournament to the user.

After a tournament has been executed its results will be shown. First there is the statistics for the tournament itself such as the total number of games played and the time data for it.

The section titled leaderboard displays the players ranked according to overall win percentage. 

The section titled Win Percentae Matrix displays the players individualized win percentages for each matchup.

At the bottom of the page there is an option to export the results of a tournament. This will be a JSON containing the displayed information that can later be uploaded to view these results.

