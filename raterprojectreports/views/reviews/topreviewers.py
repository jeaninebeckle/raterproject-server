import sqlite3
from django.shortcuts import render
from raterprojectapi.models import Review
from raterprojectreports.views import Connection


def topreviewers_count(request):
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related rating info.
            db_cursor.execute("""
                  SELECT COUNT(u.username) as count, u.username
                  FROM raterprojectapi_review r
                  JOIN raterprojectapi_game g ON r.game_id = g.id
                  JOIN raterprojectapi_player p ON r.player_id = p.id
                  JOIN auth_user u ON p.user_id = u.id
                  GROUP BY player_id
                  ORDER BY COUNT(u.username) DESC
                  LIMIT 3
            """)

            dataset = db_cursor.fetchall()

            top_reviewers = []

            for row in dataset:
                review = Review()
                review.username = row["username"]
                review.count = row["count"]

                top_reviewers.append(review)

        # Specify the Django template and provide data context
        template = 'reviews/top_reviewers.html'
        context = {
            'topreviewers_count': top_reviewers
        }

        return render(request, template, context)
