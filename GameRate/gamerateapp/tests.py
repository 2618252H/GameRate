from django.test import TestCase
import importlib
import os

# Create your tests here.

class indexTests(TestCase):
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
