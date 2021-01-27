import json
from raterprojectapi.models import Categories
from rest_framework import status
from rest_framework.test import APITestCase

class GameTests(APITestCase):
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

        categories = Categories()
        categories.label = "Strategy"
        categories.save()

    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/games"
        data = {
            "categories": [1],
            "ageRecommendation": 10,
            "title": "Clue",
            "designer": "Milton Bradley",
            "numberOfPlayers": 6,
            "yearReleased": 1980,
            "estimatedTimeToPlay": 1,
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["age_recommendation"], 10)       
        self.assertEqual(json_response["title"], "Clue")
        self.assertEqual(json_response["designer"], "Milton Bradley")
        self.assertEqual(json_response["number_of_players"], 6)
        self.assertEqual(json_response["year_released"], 1980)
        self.assertEqual(json_response["est_time_to_play"], 1)

