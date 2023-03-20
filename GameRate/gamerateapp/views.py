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
from gamerateapp.forms import UserForm, UserProfileForm, GameForm
from django.views import View

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
    
    context_dict[categories] = categories
    
    for categeroy in Category.objects.all():
        context_dict[category.str()] = Game.objects.filter(category = category)[:1].picture 
    

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
        reviews = Review.objects.order_by(game = game)
        
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
def profile(request, username):
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        user = None
    
    if user is None:
       return redirect('/gamerateapp/')
       
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'website': user_profile.website, 'picture': user_profile.picture})
    
    try:
        publisher = Publisher.objects.get(profile = user_profile)
        games = Game.objects.filter(publisher = publisher)
    except Publisher.DoesNotExist:
        games = None
    
    context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form, 'games': games}
    
    return render(request, 'gamerateapp/profile.html', context_dict)
    
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
            form.save(commit=True)
            return redirect('/gamerateapp/')
        else:
            print(form.errors)
    
    return render(request, 'gamerateapp/add_game.html', {'form':form})
    
def register(request):
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
       
    return render(request, 'gamerateapp/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
            
    else:
        return render(request, 'gamerateapp/login.html')
        
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

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