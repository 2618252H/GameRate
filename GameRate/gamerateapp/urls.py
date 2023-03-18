from django.urls import path
from gamerateapp import views

app_name = 'gamerateapp'

urlpatterns = [
	path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    path('category/<slug:category_name_slug>/', views.category, name="category"),
    path('game/<slug:game_name_slug>/', views.game, name="game"),
    path('game/<slug:game_name_slug>/review/', views.review, name="review"),
    path('profile/<username>/', views.profile, name='profile'),
    path('publisher/', views.publishers, name='publishers'),
    path('add_game/', views.add_game, name='add_game'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
