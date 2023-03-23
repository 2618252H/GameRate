from django.urls import path
from gamerateapp import views

app_name = 'gamerateapp'

urlpatterns = [
	path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    path('category/<slug:category_name_slug>/', views.category, name="category"),
    path('game/<slug:game_name_slug>/', views.game, name="game"),
    
    path('publisher/', views.publishers, name='publishers'),
    path('suggest/', views.CategorySuggestionView.as_view(), name='suggest'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<username>/register_publisher/', views.register_publisher, name='register_publisher'),
    path('profile/<username>/add_game/', views.add_game, name='add_game'),
    path('profile/<username>/game/<slug:game_name_slug>/add_review/', views.add_review, name="add_review"),
]
