import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GameRate.settings')

django.setup()

from django.contrib.auth.models import User
from gamerateapp.models import UserProfile, Publisher, Game, Category, Review

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
                  {'name': 'Adventure'},
                  {'name': 'Casual'},
                  {'name': 'MMO'},
                  {'name': 'Survival'},
                  {'name': 'PvP'},
                  {'name': 'Action'},
                  {'name': 'Simulation'},
                  ]
    
    games = [{'name': 'Game1',
            'publisher':'publisher1',
            'game_Description': 'Game1 Description',
            'category': 'RPG',
            'story_rating': 10,
            'gameplay_rating': 7,
            'graphics_rating': 8,
            'difficulty_rating': 10,},
             {'name': 'Game2',
                     'publisher':'publisher1',
                     'game_Description': 'Game2 Description',
                     'category': 'PvP',
                     'story_rating': 8,
                     'gameplay_rating': 5,
                     'graphics_rating': 9,
                     'difficulty_rating': 10,},
             {'name': 'Game3',
                     'publisher':'publisher2',
                     'game_Description': 'Game3 Description',
                     'category': 'Action',
                     'story_rating': 4,
                     'gameplay_rating': 10,
                     'graphics_rating': 10,
                     'difficulty_rating': 6,},
             ]
    
    reviews= [{
            'user': 'user123',
            'game': 'Game1',
            'title': 'Review1',
            'comments': 'Review1 Comments',
            'story_rating': 10,
            'gameplay_rating': 10,
            'graphics_rating': 10,
            'difficulty_rating': 10,},
        {
                'user': 'user234',
                'game': 'Game2',
                'title': 'Review1',
                'comments': 'Review1 Comments',
                'story_rating': 5,
                'gameplay_rating': 6,
                'graphics_rating': 7,
                'difficulty_rating': 8,},
        {
                'user': 'user234',
                'game': 'Game1',
                'title': 'Review2',
                'comments': 'Review1 Comments',
                'story_rating': 1,
                'gameplay_rating': 8,
                'graphics_rating': 5,
                'difficulty_rating': 6,},
        {
                'user': 'user123',
                'game': 'Game3',
                'title': 'Review1',
                'comments': 'Review1 Comments',
                'story_rating': 5,
                'gameplay_rating': 4,
                'graphics_rating': 9,
                'difficulty_rating': 10,},
        
        ]
    
    for user in users:
        users = add_user(user['username'], user['email'], user['password'])
        add_userprofile(users)
    
    for publisher in publishers:
        publishers = add_user(publisher['name'], publisher['email'], publisher['password'])
        add_publishers(publishers)
    
    for category in categories:
        add_category(category['name'])
        
    for game in games:
        add_game(game['name'], game['publisher'], game['game_Description'], 
                 game['category'], game['story_rating'], game['gameplay_rating'],
                 game['graphics_rating'], game['difficulty_rating'])
    
    for review in reviews:
        add_review(review['user'],review['game'],review['title'],review['comments'],
                   review['story_rating'],review['gameplay_rating'],review['graphics_rating'],review['difficulty_rating'],)


def add_user (username, email, password):
    user = User.objects.create_user(username=username, password=password)
    user.save()
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
    
    g.save()
    return g

def add_review(user, game, title, comments, story_rating, gameplay_rating,
                graphics_rating, difficulty_rating):
    
    user_name= User.objects.get(username = user)
    game_name= Game.objects.get(name = game)
    
    r = Review.objects.get_or_create(user = user_name, game= game_name , title = title)[0]
    
    r.comments = comments
    r.story_rating = story_rating
    r.gameplay_rating = gameplay_rating
    r.graphics_rating = graphics_rating
    r.difficulty_rating = difficulty_rating
    
    r.save()
    return r

if __name__ == '__main__':
    print('starting populate')
    populate()