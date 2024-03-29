from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images',default = 'profile_images/default.png', blank=True)
    
    def __str__(self):
        return self.user.username

class Publisher(models.Model):
    
    profile = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.profile.__str__()
        
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'categories'

    
    def __str__(self):
        return self.name
        
class Game(models.Model):
    name = models.CharField(max_length=128, unique=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    game_Description = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    story_rating = models.IntegerField(default = 0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    gameplay_rating = models.IntegerField(default = 0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    graphics_rating = models.IntegerField(default = 0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    difficulty_rating = models.IntegerField(default = 0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    picture = models.ImageField(upload_to='game_images',default='game_images/no_image.jpg', blank=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'Games'
    
    def __str__(self):
        return self.name
        
class Review(models.Model):
    
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    game = models.ForeignKey(Game, on_delete = models.CASCADE)
    title = models.CharField(max_length=128)
    comments = models.CharField(max_length=128)
    story_rating = models.IntegerField(default = 0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    gameplay_rating = models.IntegerField(default = 0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    graphics_rating = models.IntegerField(default = 0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    difficulty_rating = models.IntegerField(default = 0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    
    def __str__(self):
        return self.title