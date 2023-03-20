import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GameRate.settings')
django.setup()

from django.contrib.auth.models import User
from gamerateapp.models import UserProfile, Publisher, Category, Game, Review

def populate():
    # create users
    users = [
        {'username': 'user1', 'website': 'user1@example.com', 'picture':'picture'}, #add more users

    ]
    publishers = [
        {'name': 'Publisher1'},  # add more publishers here
    ]

    categories = [
        {'name': 'RPG'},{'name':'singlePlayer'},
        {'name': 'multiplayer'}
    ]

    games = [
        {
            'name': 'Game1',
            'publisher': 'publisher1'),
            'game_Description': 'Game1 Description',
            'category': 'action'),
            'story_rating': 10,
            'gameplay_rating': 10,
            'graphics_rating': 10,
            'difficulty_rating': 10,
        }]

    reviews = [
        {
            'user': 'user1'),
            'game': 'user',
            'title': 'Review1',
            'pub_date': 'date',
            'comments': 'Review1 Comments',
            'story_rating': 10,
            'gameplay_rating': 10,
            'graphics_rating': 10,
            'difficulty_rating': 10,
        }]




#function to add new users

    for user, user_date in users.items():
    
        U = add_user(users['username'], users['website'], users['picture'] 
    
    
  
    


def add_user(user, website, picture):

    u = UserProfile.objects.get_or_Create(user=user)[0]
    u.website = website
    u.picture = picture

    u.save()

    return u



def add_game(name, publisher, gameDesc, cat, story, gameplay, graphics, diff):

    g = Game.objects.get_or_create(name=name)[0]

    g.publisher = publisher
    g.publisher = publisher
    g.game_Description = gameDesc
    g.category = cat
    g.story_rating = story
    g.graphics_rating = graphics
    g.gameplay = gameplay
    g.difficulty = diff

    g.save()

    return g

def add_publisher(profile):

    p = publisher.objects.get_or_create(profile=profile)[0]

    p.save()

    return p


def add_review(user, game, title, date, comment, story, gameplay, graphics, difficulty):
    r = Review.objects.get_or_create(user=user)[0]
    r.game = game
    r.title = title
    r.pub_date = date
    r.comments = comment
    r.story_rating = story
    r.gameplay_rating = gameplay
    r.graphics_rating = graphics
    r.difficulty_rating = difficulty

    r.save()

    return r


def add_category(category):
    c = Category.objects.get_or_create(category=category)[0]

    c.save()

    return c

if __name__ == '__main__':
    print('starting populate')
    populate()
