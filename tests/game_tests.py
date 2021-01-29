import json

from raterprojectapi.models import Categories, Game
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

    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """
        game = Game()
        game.title = "Sorry"
        game.description = "Very fun"
        game.year_released = 1970
        game.designer = "Milton Bradley"
        game.number_of_players = 4
        game.est_time_to_play = 1
        game.age_recommendation = 6
        game.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "title": "Sorry",
            "description": "Actually only kind of fun",
            "yearReleased": 1970,
            "designer": "Hasbro",
            "numberOfPlayers": 4,
            "estimatedTimeToPlay": 2,
            "ageRecommendation": 6
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["title"], "Sorry")
        self.assertEqual(json_response["description"], "Actually only kind of fun")
        self.assertEqual(json_response["year_released"], 1970)
        self.assertEqual(json_response["designer"], "Hasbro")
        self.assertEqual(json_response["number_of_players"], 4) 
        self.assertEqual(json_response["est_time_to_play"], 2)
        self.assertEqual(json_response["age_recommendation"], 6)

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.title = "Sorry"
        game.description = "Very fun"
        game.year_released = 1970
        game.designer = "Milton Bradley"
        game.number_of_players = 4
        game.est_time_to_play = 1
        game.age_recommendation = 6
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_game(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        game = Game()
        game.title = "Sorry"
        game.description = "Very fun"
        game.year_released = 1970
        game.designer = "Milton Bradley"
        game.number_of_players = 4
        game.est_time_to_play = 1
        game.age_recommendation = 6
        game.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/games/{game.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["title"], "Sorry")
        self.assertEqual(json_response["description"], "Very fun")
        self.assertEqual(json_response["year_released"], 1970)
        self.assertEqual(json_response["designer"], "Milton Bradley")
        self.assertEqual(json_response["number_of_players"], 4) 
        self.assertEqual(json_response["est_time_to_play"], 1)
        self.assertEqual(json_response["age_recommendation"], 6)

    def test_get_all_games(self):
        """
        Ensure we can get all games.
        """

        # Seed the database with a game
        for i in range(2):
          game = Game()
          game.title = "Sorry"
          game.description = "Very fun"
          game.year_released = 1970
          game.designer = "Milton Bradley"
          game.number_of_players = 4
          game.est_time_to_play = 1
          game.age_recommendation = 6
          game.save()

        # game = Game()
        # game.title = "Clue"
        # game.description = "For mystery lovers and problem solvers"
        # game.year_released = 1980
        # game.designer = "Hasbro"
        # game.number_of_players = 6
        # game.est_time_to_play = 2
        # game.age_recommendation = 10
        # game.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/games")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        for i in range(2):
          self.assertEqual(json_response[i]["title"], "Sorry")
          self.assertEqual(json_response[i]["description"], "Very fun")
          self.assertEqual(json_response[i]["year_released"], 1970)
          self.assertEqual(json_response[i]["designer"], "Milton Bradley")
          self.assertEqual(json_response[i]["number_of_players"], 4) 
          self.assertEqual(json_response[i]["est_time_to_play"], 1)
          self.assertEqual(json_response[i]["age_recommendation"], 6)

