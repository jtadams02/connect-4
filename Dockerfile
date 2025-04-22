FROM python:3.13-slim

WORKDIR /app

RUN mkdir ./connect4/

COPY src/connect4/game_engine.py src/connect4/tournament.py ./connect4/