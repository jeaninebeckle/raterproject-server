"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from raterprojectapi.models import Game
from raterprojectreports.views import Connection


def bottomgamerating_list(request):
    """Function to build an HTML report of games by rating"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related rating info.
            db_cursor.execute("""
                SELECT
                    g.id,
                    g.title,
                    AVG(r.value) AS average_rating
                FROM
                    raterprojectapi_game g
                JOIN
                    raterprojectapi_rating r ON r.game_id = g.id
                GROUP BY g.title
                ORDER BY average_rating ASC
                LIMIT 5
            """)

            dataset = db_cursor.fetchall()

            bottom_games_by_rating = []

            for row in dataset:
                # Create a Game instance and set its properties. String in brackets matches the SQL results
                game = Game()
                game.title = row["title"]
                game.rating = row["average_rating"]

                bottom_games_by_rating.append(game)

        # Specify the Django template and provide data context
        template = 'ratings/list_with_lowest_ratings.html'
        context = {
            'bottomgamerating_list': bottom_games_by_rating
        }

        return render(request, template, context)
