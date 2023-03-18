import importlib
import os
from django.test import TestCase
from django.urls import reverse
from gamerateapp.models import Category, Game, Review, UserProfile

class projectStructureTests(TestCase):
    def setup(self):
        self.project_base_dir = os.getcwd()
        self.gamerate_app_dir = os.path.join(self.project_base_dir, "gamerateapp")

    def testProjectCreated(self):
        directory_exists = os.path.isdir(os.path.join(self.project_base_dir, "GameRate"))
        urls_module_exists = os.path.isFile(os.path.join(self.project_base_dir, "GameRate", "urls.py"))
    
        self.assertTrue(directory_exists, "Directory Test Failed")
        self.assertTrue(urls_module_exists, "url File Test Failed")

    def testGameRateAppCreated(self):
        directory_exists = os.path.isdir(self.gamerate_app_dir)
        is_python_package = os.path.isfile(os.path.join(self.gamerate_app_dir, '__init__.py'))

        self.assertTrue(directory_exists, "Directory Test Failed")
        self.assertTrue(is_python_package, "Directory Missing Files")

class indexTests(TestCase):
    def setup(self):
        self.views_module = importlib.import_module('gamerateapp.views')
        self.views_module_listing = dir(self.views_module)
        self.project_urls_module = importlib.import_module('GameRate.urls')

    def viewsExists(self):
        name_exists = 'index' in self.views_module_listing
        is_callable = callable(self.views_module.index)
        
        self.assertTrue(name_exists, "The index() view for GameRate does not exist")
        self.assertTrue(is_callable, "Check that you have created the index() view correctly")
    
    def response(self):
        response = self.client.get(reverse('gamerateapp:index'))

        self.assertEqual(response.status_code, 200, "Requesting the index page failed")
        self.assertContains(response, "GameRate Home Page", msg_prefix="The index view does not return the expected response")

class categoryTests(TestCase):
    def setup(self):
        self.views_module = importlib.import_module('gamerateapp.views')
        self.views_module_listing = dir(self.views_module)
    
    def viewsExists(self):
        name_exists = 'category' in self.views_module_listing
        is_callable = callable(self.views_module.category)
        
        self.assertTrue(name_exists, "The category view for GameRate does not exist")
        self.assertTrue(is_callable, "Check that you have created the category view correctly")

    def response(self):
        response = self.client.get(reverse('gamerateapp:category'))

        self.assertEqual(response.status_code, 200, "Requesting the category page failed")

class modelTest(TestCase):
    def setup(self):
        Category.objects.get_or_create(name='Action')
        game1 = Game.objects.get_or_create(name='game 1', publisher='bob', game_Description='game description', category='Action')
        user1 = UserProfile.objects.get_or_create(user=' ')
        Review.objects.get_or_create(user=user1, game=game1, title='review 1', story_rating=5, graphics_rating=8)

    def test_game_model(self):
        game_py = Game.objects.get(name='game 1')
        self.assertEqual(game_py.game_Description, 'game description', "Tests on the Game model failed")
        self.assertEqual(game_py.category, 'Action', "Tests on the Game model failed")
    
    def test_review_model(self):
        review_py = Review.objects.get(title='review 1')
        self.assertEqual(review_py.story_rating, 5, "Tests on the Review model failed")
        self.assertEqual(review_py.graphics_rating, 8, "Tests on the Review model failed")


        