from django.urls import path
from gamerateapp import views

app_name = 'gamerateapp'

urlpatterns = [
	path('', views.index, name='index'),
    path('categories/', view.categories, name='categories'),
    path('category/<slug:category_name_slug>/' views.category, name="category"),
    path('game/<slug:game_name_slug>/' views.game, name="game"),
    path('game/<slug:game_name_slug>/review/' view.review, name="review"),
    path('profile/<username>/', views.profile, name='profile'),
    path('publisher/', view.publishers, name='publishers'),
]
