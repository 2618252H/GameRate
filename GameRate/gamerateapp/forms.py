from django import forms
from gamerateapp.models import UserProfile, Publisher, Game, Review
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)

class PublisherForm(forms.ModelForm):
    
    class Meta:
        model = Publisher
        fields = ('website','profile', 'picture',)

class GameForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text= "What is the name of the game?")
    
    class Meta:
        model = Game
        fields = ('name', 'picture', 'publisher','category', 'game_Description')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'comments', 'story_rating', 'gameplay_rating', 
                  'graphics_rating', 'difficulty_rating')