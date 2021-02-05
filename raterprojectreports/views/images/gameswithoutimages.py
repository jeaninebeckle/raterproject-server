import sqlite3
from django.shortcuts import render
from raterprojectapi.models import Game
from raterprojectreports.views import Connection


def gameswithoutimages(request):
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related rating info.
            db_cursor.execute("""
              SELECT 
                COUNT(g.title) as number
                FROM raterprojectapi_game g
                LEFT JOIN raterprojectapi_gamepicture p on g.id = p.game_id
                WHERE p.game_id is null
            """)

            dataset = db_cursor.fetchall()

            games_without_images = []

            for row in dataset:
                # Create a Game instance and set its properties. String in brackets matches the SQL results
                game = Game()
                game.count = row["number"]
                games_without_images.append(game)

        # Specify the Django template and provide data context
        template = 'images/number_games_no_images.html'
        context = {
            'gameswithoutimages': games_without_images
        }

        return render(request, template, context)
