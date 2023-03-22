import importlib
import os
import warnings
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.db.models.query import QuerySet
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

    def contextDictionary(self):
        expected_top_gameplay = list(Game.objects.order_by('-gameplay_rating')[:1])
        expected_top_graphics = list(Game.objects.order_by('-gameplay_rating')[:1])

        self.assertTrue('top_gameplay' in self.response.context, "The 'top_gameplay' variable couldn't be found in the context dictionary for the index() view")
        self.assertEquals(expected_top_gameplay, self.response.context['top_gameplay'], "top_gameplay is not in the index view")
        
        self.assertTrue('top_graphics' in self.response.context, "The 'top_graphics' variable couldn't be found in the context dictionary for the index() view")
        self.assertEquals(expected_top_graphics, self.response.context['top_graphics'], "top_graphics is not in the index view")
        
    def responseTitles(self):
        expected_top_gameplay = '<h2>Top in Gameplay</h2>'
        expected_top_difficulty = '<h2>Top in Difficulty</h2>'

        self.assertIn(expected_top_gameplay, self.content, "Couldn't find the markup for top gameplay")
        self.assertIn(expected_top_difficulty, self.content, "Couldn't find the markup for top difficulty")

    def emptyIndexTitles(self):
        self.assertEqual(type(self.response.context['top_publishers']), QuerySet, "The top_publishers variable in the context dictionary yields a QuerySet object")
        self.assertEqual(len(self.response.context['top_publishers']), 0, "The top_publishers variable is not empty")

        self.assertEqual(type(self.response.context['top_story']), QuerySet, "The top_story variable in the context dictionary yields a QuerySet object")
        self.assertEqual(len(self.response.context['top_story']), 0, "The top_story variable is not empty")


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


class databaseTest(TestCase):
    def setup(self):
        pass

    def database_variable_exists(self):
        self.assertTrue(settings.DATABASES, "Project's settings module does not have a DATABASES variable")
        self.assertTrue('default' in settings.DATABASES, "There is no 'default' database configuration in the project's DATABASES configuration variable")


class formsTest(TestCase):
    def game_form(self):
        import gamerateapp.forms
        self.assertTrue('GameForm' in dir(gamerateapp.forms), "game form not found")

        from gamerateapp.forms import GameForm
        game_form = GameForm()

        self.assertEqual(type(game_form.__dict__['instance']), Game, "game form doesn't link to game model")

        fields = game_form.fields
        

# class populationScriptTest(TestCase):
#     def setup(self):
#         try:
#             import populate_