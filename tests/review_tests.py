import json

from raterprojectapi.models import Game, Player
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class ReviewTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        game = Game()
        game.title = "Clue"
        game.number_of_players = 6
        game.est_time_to_play = 1
        game.age_recommendation = 10
        game.designer = "Milton Bradley"
        game.year_released = 1980
        game.save()

        user = User()
        user.save()

        player = Player()
        player.user = user
        player.save()

    def test_create_review(self):
        """
        Ensure we can create a new review.
        """
        # DEFINE REVIEW PROPERTIES
        url = "/reviews"
        data = {
            "description": "Lorem ipsum",
            "game": 1,
            "player": 1,
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the review was created
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["description"], "Lorem ipsum")    
        self.assertEqual(json_response["game"], 1)   
        self.assertEqual(json_response["player"], 1)
