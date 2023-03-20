import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')
django.setup()


from models import UserProfile, Publisher, Category, Game, Review

def populate():
    # create users
    users = [
        {'username': 'user1', 'email': 'user1@example.com', 'password': 'password1'}, #add more users

    ]
    for user_data in users:
        user = User.objects.create_user(**user_data)
        UserProfile.objects.create(user=user, website='http://google.com')

    # create publishers
    publishers = [
        {'name': 'Publisher1'}, #add more publishers here
    ]
    for publisher_data in publishers:
        profile = UserProfile.objects.create(user=User.objects.create_user(
            username=publisher_data['name'], password='password'))
        Publisher.objects.create(profile=profile)

    # create categories
    categories = [
        {'name': 'RPG'}, #add in categories
    ]
    for category_data in categories:
        Category.objects.create(**category_data)

    # create games
    games = [
        {
            'name': 'Game1',
            'publisher': Publisher.objects.get(profile__user__username='Publisher1'),
            'game_Description': 'Game1 Description',
            'category': Category.objects.get(name='Action'),
            'story_rating': 10,
            'gameplay_rating': 10,
            'graphics_rating': 10,
            'difficulty_rating': 10,
        },

    ]
    for game_data in games:
        Game.objects.create(**game_data)

    # create reviews
    reviews = [
        {
            'user': UserProfile.objects.get(user__username='user1'),
            'game': Game.objects.get(name='Game1'),
            'title': 'Review1',
            'pub_date': 'date',
            'comments': 'Review1 Comments',
            'story_rating': 10,
            'gameplay_rating': 10,
            'graphics_rating': 10,
            'difficulty_rating': 10,
        }]

#function to add new users

def add_user(username, password, email):

    user = user.objects.get_or_create(username=username, password=password, email=email)

    user_profile = UserProfile(user=user)

    user_profile.save()

    return user


if __name__ == '__main__':
    print('starting populate')
    populate()
