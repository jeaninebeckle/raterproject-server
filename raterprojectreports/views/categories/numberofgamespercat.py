"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from raterprojectapi.models import Categories
from raterprojectreports.views import Connection


def gamecategory_list(request):
    """Function to build an HTML report of number of games per category"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related rating info.
            db_cursor.execute("""
                SELECT 
                  c.label,
                  COUNT(g.title) as number
                FROM raterprojectapi_categories c
                JOIN 
                  raterprojectapi_game_categories gc on gc.categories_id = c.id
                JOIN 
                  raterprojectapi_game g on gc.game_id = g.id
                GROUP BY c.label
            """)

            dataset = db_cursor.fetchall()

            number_games_per_cat = []

            for row in dataset:
                # Create a Game instance and set its properties. String in brackets matches the SQL results
                categories = Categories()
                categories.label = row["label"]
                categories.count = row["number"]

                number_games_per_cat.append(categories)

        # Specify the Django template and provide data context
        template = 'categories/number_of_games_per_category.html'
        context = {
            'gamecategory_list': number_games_per_cat
        }

        return render(request, template, context)
