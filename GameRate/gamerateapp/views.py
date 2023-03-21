from django.shortcuts import render, redirect
from django.http import HttpResponse
from gamerateapp.models import Game
from gamerateapp.models import Category
from gamerateapp.models import Review, User, Publisher, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from gamerateapp.forms import ReviewForm
from django.urls import reverse
from django.shortcuts import redirect
from gamerateapp.forms import UserForm, UserProfileForm, GameForm, PublisherForm
from django.views import View
from django.contrib.auth.models import User
from gamerateapp.models import UserProfile
from django.utils.decorators import method_decorator

# Create your views here.

def index(request):

    top_gameplay = Game.objects.order_by('-gameplay_rating')[:1]
    top_graphics = Game.objects.order_by('-graphics_rating')[:1]
    top_story = Game.objects.order_by('-story_rating')[:1]
    top_difficulty = Game.objects.order_by('-difficulty_rating')[:1]
    
    context_dict = {}
    context_dict['top_gameplay'] = top_gameplay
    context_dict['top_graphics'] = top_graphics
    context_dict['top_story'] = top_story
    context_dict['top_difficulty'] = top_difficulty
    
    
    response = render(request, 'gamerateapp/index.html', context=context_dict)
    
    return response
    
def categories(request):

    context_dict = {}
    
    categories = Category.objects.all()
    
    context_dict['categories'] = categories

    response = render(request, 'gamerateapp/categories.html', context=context_dict)
    
    return response
    
def category(request, category_name_slug):

    context_dict = {}
    
    try:
        category = Category.objects.get(slug=category_name_slug)
        games = Game.objects.filter(category = category)
        
        context_dict['games'] = games
        context_dict['category'] = category
        
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['games'] = None
    
    
    response = render(request, 'gamerateapp/category.html', context=context_dict)
    
    return response
    
def game(request, game_name_slug):

    context_dict = {}

    try:
        game = Game.objects.get(slug=game_name_slug)
        reviews = Review.objects.filter(game = game)
        
        context_dict['game'] = game
        context_dict['reviews'] = reviews
        
    except Game.DoesNotExist:
        context_dict['game'] = None
        
    
    
    response = render(request, 'gamerateapp/game.html', context=context_dict)
    return response

@login_required
def review(request, game_name_slug):
    try:
        game = Game.objects.get(slug=game_name_slug)
    except Game.DoesNotExist:
        game = None
    
    if game is None:
        return redirect('/gamerateapp/')
    
    form = ReviewForm()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            if game:
                review = form.save(commit=False)
                review.game = game
                review.save()
                
                return redirect(reverse('gamerateapp:game', kwargs={'game_name_slug': game_name_slug}))
        else:
            print(form.errors)
    
    context_dict = {'form': form, 'game': game}
    return render(request, 'gamerateapp/review.html', context=context_dict)
    
@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect(reverse('gamerateapp:index'))
        else:
            print(form.errors)
    context_dict = {'form': form}
    return render(request, 'gamerateapp/profile_registration.html', context_dict)
    
def register_publisher(request):
    form = PublisherForm()
    if request.method == 'POST':
        form = PublisherForm(request.POST, request.FILES)
        if form.is_valid():
            publisher_profile = form.save(commit=False)
            publisher_profile.profile = request.user
            publisher_profile.save()
            return redirect(reverse('gamerateapp:index'))
        else:
            print(form.errors)
    context_dict = {'form':form}
    return render(request, 'gamerateapp/publisher_registration.html', context_dict)
    
    
def publishers(request):
    
    context_dict = {}
    
    publishers = Publisher.objects.all()
    
    context_dict['publishers'] = publishers

    
    return render(request, 'gamerateapp/publishers.html', context_dict)
   
@login_required
def add_game(request):
    form = GameForm()
    
    if request.method == 'POST':
        form = GameForm(request.POST)
        
        if form.is_valid():
            game = form.save(commit=True)
            
            if 'picture' in request.FILES:
                game.picture = request.FILES['picture']
                
            return redirect('/gamerateapp/')
        else:
            print(form.errors)
    
    return render(request, 'gamerateapp/add_game.html', {'form':form})

def get_search_list(max_results=0, starts_with=''):
    category_list = []
    publisher_list = []
    game_list = []
    search_list = []
    if starts_with:
        category_list = Category.objects.filter(name__istartswith=starts_with)
        publisher_list = Publisher.objects.filter(name__istartswith=starts_with)
        game_list = Game.objects.filter(name__istartswith=starts_with)
        search_list = category_list + publisher_list + game_list
        
    if max_results > 0:
        if len(search_list) > max_results:
            search_list = search_list[:max_results]
    return search_list

class CategorySuggestionView(View):
    def get(self, request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''
            
        search_list = get_search_list(max_results=8, starts_with=suggestion)
        
        if len(search_list) == 0:
            category_list = Category.objects.order_by('-name')
            publisher_list = Publisher.objects.order_by('profile.__Str__()')
            game_list = Game.objects.order_by('-name')
            search_list = category_list + publisher_list + game_list
            
            return render(request, 'gamerateapp/categories.html', {'categories': search_list})
        
class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': user_profile.website, 'picture': user_profile.picture})

            
        return (user, user_profile, form)

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('gamerateapp:index'))
            
        try:
            publisher = Publisher.objects.get(profile = user)
        except Publisher.DoesNotExist:
            publisher = None
            
        context_dict = {'user_profile': user_profile,'selected_user': user,'form': form, 'publisher':publisher}
        return render(request, 'gamerateapp/profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('gamerateapp:index'))
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('gamerateapp:profile', user.username)
        else:
            print(form.errors)
            
        try:
            publisher = Publisher.objects.get(profile = user)
        except Publisher.DoesNotExist:
            publisher = None
            
        context_dict = {'user_profile': user_profile,'selected_user': user,'form': form, 'publisher':publisher}
    
        return render(request, 'gamerateapp/profile.html', context_dict)
