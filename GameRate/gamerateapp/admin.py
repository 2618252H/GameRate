from django.contrib import admin
from gamerateapp.models import Game,Category,Review

# Register your models here.

admin.site.register(Game)
admin.site.register(Category)
admin.site.register(Review)