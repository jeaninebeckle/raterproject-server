import sqlite3
from django.shortcuts import render
from raterprojectapi.models import Game
from raterprojectreports.views import Connection


def suitableforkids_list(request):
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related rating info.
            db_cursor.execute("""
              SELECT 
                g.title,
                g.age_recommendation
              FROM raterprojectapi_game g
              WHERE g.age_recommendation < 8
            """)

            dataset = db_cursor.fetchall()

            games_for_kids_under_8 = []

            for row in dataset:
                # Create a Game instance and set its properties. String in brackets matches the SQL results
                game = Game()
                game.title = row["title"]
                game.age_recommendation = row["age_recommendation"]

                games_for_kids_under_8.append(game)

        # Specify the Django template and provide data context
        template = 'players/suitable_for_kids.html'
        context = {
            'suitableforkids_list': games_for_kids_under_8
        }

        return render(request, template, context)
