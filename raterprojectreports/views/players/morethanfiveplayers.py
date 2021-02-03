import sqlite3
from django.shortcuts import render
from raterprojectapi.models import Game
from raterprojectreports.views import Connection


def numberofplayers_list(request):
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related rating info.
            db_cursor.execute("""
              SELECT 
                g.number_of_players,
                g.title
              FROM raterprojectapi_game g
              WHERE g.number_of_players > 5
            """)

            dataset = db_cursor.fetchall()

            games_with_5_plus_players = []

            for row in dataset:
                # Create a Game instance and set its properties. String in brackets matches the SQL results
                game = Game()
                game.title = row["title"]
                game.number_of_players = row["number_of_players"]

                games_with_5_plus_players.append(game)

        # Specify the Django template and provide data context
        template = 'players/list_with_5plus_players.html'
        context = {
            'numberofplayers_list': games_with_5_plus_players
        }

        return render(request, template, context)
