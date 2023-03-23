import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GameRate.settings')

django.setup()

from django.contrib.auth.models import User
from gamerateapp.models import UserProfile, Publisher, Game, Category

def populate():
    
    users = [{'username': 'user123', 'email':'lennon@thebeatles.com', 'password': 'johnpassword'},
             {'username': 'user234', 'email':'lennon@thebeatles.com', 'password': 'johnpassword'},
             {'username': 'user345', 'email':'lennon@thebeatles.com', 'password': 'johnpassword'},
             {'username': 'user456', 'email':'lennon@thebeatles.com', 'password': 'johnpassword'},]
    
    publishers = [{'name': 'publisher1', 'email':'lennon@thebeatles.com', 'password': 'johnpassword'},
                  {'name': 'publisher2', 'email':'lennon@thebeatles.com', 'password': 'johnpassword'},
                  {'name': 'publisher3', 'email':'lennon@thebeatles.com', 'password': 'johnpassword'},
                  {'name': 'publisher4', 'email':'lennon@thebeatles.com', 'password': 'johnpassword'},
                  ]

    categories = [{'name': 'RPG'},
                  {'name': 'SinglePlayer'},
                  {'name': 'MultiPlayer'},
                  ]
    
    games = [{'name': 'Game1',
            'publisher':'publisher1',
            'game_Description': 'Game1 Description',
            'category': 'RPG',
            'story_rating': 10,
            'gameplay_rating': 10,
            'graphics_rating': 10,
            'difficulty_rating': 10,}]
    
    for user in users:
        users = add_user(user['username'], user['email'], user['password'])
        add_userprofile(users)
    
    for publisher in publishers:
        publishers = add_user(publisher['name'], publisher['email'], publisher['password'])
        add_publishers(publishers)
        print(Publisher.profile)
    
    for category in categories:
        add_category(category['name'])
        
    for game in games:
        add_game(game['name'], game['publisher'], game['game_Description'], 
                 game['category'], game['story_rating'], game['gameplay_rating'],
                 game['graphics_rating'], game['difficulty_rating'])


def add_user (username, email, password):
    user = User.objects.create_user(username=username, password=password)
    return user

def add_userprofile (user):
    u = UserProfile.objects.get_or_create(user=user)[0]
    u.save()
    return u

def add_publishers (user):
    p = Publisher.objects.get_or_create(profile=user)[0]
    p.save()
    return p

def add_category(name):
    c = Category.objects.get_or_create(name = name)[0]
    c.save()
    return c

def add_game(name, publisher, game_Description, category, story_rating,
             gameplay_rating, graphics_rating, difficulty_rating):
    
    publisher_name = Publisher.objects.get(profile__username = publisher)
    category_name= Category.objects.get(name = category)
    
    g = Game.objects.get_or_create(name = name, publisher = publisher_name, category = category_name)[0]
    
    g.game_Description = game_Description
    g.story_rating = story_rating
    g.graphics_rating = graphics_rating
    g.gameplay_rating = gameplay_rating
    g.difficulty_rating = difficulty_rating
    
    return g

if __name__ == '__main__':
    print('starting populate')
    populate()