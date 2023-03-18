from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    def __str__(self):
        return self.user.username

class Publisher(models.Model):
    
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key = True)
    
    def __str__(self):
        return self.profile.str()
        
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
        
class Game(models.Model):
    name = models.CharField(max_length=128, unique=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    game_Description = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    story_rating = models.IntegerField(default = 0)
    gameplay_rating = models.IntegerField(default = 0)
    graphics_rating = models.IntegerField(default = 0)
    difficulty_rating = models.IntegerField(default = 0)
    picture = models.ImageField(upload_to='game_images', blank=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
        
class Review(models.Model):
    
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    game = models.ForeignKey(Game, on_delete = models.CASCADE)
    title = models.CharField(max_length=128)
    pub_date = models.DateTimeField('date published')
    comments = models.CharField(max_length=128)
    story_rating = models.IntegerField(default = 0)
    gameplay_rating = models.IntegerField(default = 0)
    graphics_rating = models.IntegerField(default = 0)
    difficulty_rating = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.title