from django.contrib import admin
from gamerateapp.models import Game,Category,Review,UserProfile,Publisher

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Publisher)
admin.site.register(Game)
admin.site.register(Category)
admin.site.register(Review)