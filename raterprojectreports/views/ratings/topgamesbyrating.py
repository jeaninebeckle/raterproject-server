"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from raterprojectapi.models import Game
from raterprojectreports.views import Connection


def topgamerating_list(request):
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
                ORDER BY average_rating DESC
            """)

            dataset = db_cursor.fetchall()

            games_by_rating = []

            for row in dataset:
                # Create a Game instance and set its properties. String in brackets matches the SQL results
                game = Game()
                game.title = row["title"]
                game.rating = row["average_rating"]

                games_by_rating.append(game)

        #         # Store the user's id
        #         uid = row["user_id"]

        #         # If the user's id is already a key in the dictionary...
        #         if uid in games_by_user:

        #             # Add the current game to the `games` list for it
        #             games_by_user[uid]['games'].append(game)

        #         else:
        #             # Otherwise, create the key and dictionary value
        #             games_by_user[uid] = {}
        #             games_by_user[uid]["id"] = uid
        #             games_by_user[uid]["full_name"] = row["full_name"]
        #             games_by_user[uid]["games"] = [game]

        # # Get only the values from the dictionary and create a list from them
        # list_of_top_games_by_rating = games_by_user.values()

        # Specify the Django template and provide data context
        template = 'ratings/list_with_top_ratings.html'
        context = {
            'gamerating_list': games_by_rating
        }

        return render(request, template, context)
