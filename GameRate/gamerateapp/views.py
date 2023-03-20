from django.shortcuts import render, redirect
from django.http import HttpResponse
from gamerateapp.models import Game
from gamerateapp.models import Category
from gamerateapp.models import Review, User, Publisher, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from gamerateapp.forms import ReviewForm
from django.urls import reverse
from gamerateapp.forms import UserForm, UserProfileForm, GameForm
from django.views import View
from gamerateapp.forms import UserProfileForm
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from gamerateapp.models import UserProfile


from gamerateapp.forms import UserProfileForm
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from gamerateapp.models import UserProfile


>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
    return response
=======
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

def publishers(request):

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
                return redirect(reverse('gamerateapp:index'))
                return redirect(reverse('gamerateapp:index'))
            else:
                return HttpResponse("Your GameRate account is disabled.")
                return HttpResponse("Your GameRate account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
            
    else:
        return render(request, 'gamerateapp/login.html')
        
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('gamerateapp:index'))
    return redirect(reverse('gamerateapp:index'))

def get_category_list(max_results=0, starts_with=''):
    category_list = []
    if starts_with:
        category_list = Category.objects.filter(name__istartswith=starts_with)
        
    if max_results > 0:
        if len(category_list) > max_results:
            category_list = category_list[:max_results]
    return category_list

class CategorySuggestionView(View):
    def get(self, request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''
            
        category_list = get_category_list(max_results=8, starts_with=suggestion)
        
        if len(category_list) == 0:
            category_list = Category.objects.order_by('-likes')
            
            return render(request, 'gamerateapp/categories.html', {'categories': category_list})

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
        context_dict = {'user_profile': user_profile,'selected_user': user,'form': form}
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
        
        context_dict = {'user_profile': user_profile,'selected_user': user,'form': form}
    
        return render(request, 'gamerateapp/profile.html', context_dict)

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
        context_dict = {'user_profile': user_profile,'selected_user': user,'form': form}
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
        
        context_dict = {'user_profile': user_profile,'selected_user': user,'form': form}
    
        return render(request, 'gamerateapp/profile.html', context_dict)
>>>>>>> Stashed changes
