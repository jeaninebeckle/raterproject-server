import sqlite3
from django.shortcuts import render
from raterprojectapi.models import Game
from raterprojectreports.views import Connection


def mostreviewedgametitle(request):
    """Function to build an HTML report of games by rating"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related rating info.
            db_cursor.execute("""
                SELECT 
                  g.title,
                  COUNT(g.id) as number
                FROM raterprojectapi_game g
                JOIN raterprojectapi_review r ON r.game_id = g.id
                GROUP BY g.id
                ORDER BY COUNT(g.id) DESC
                LIMIT 1
            """)

            dataset = db_cursor.fetchall()

            most_reviewed_game = []

            for row in dataset:
                # Create a Game instance and set its properties. String in brackets matches the SQL results
                game = Game()
                game.title = row["title"]
                game.review = row["number"]

                most_reviewed_game.append(game)

        # Specify the Django template and provide data context
        template = 'reviews/most_reviewed_game.html'
        context = {
            'mostreviewedgametitle': most_reviewed_game
        }

        return render(request, template, context)
