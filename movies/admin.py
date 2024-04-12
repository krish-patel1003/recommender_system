from django.contrib import admin
from movies.models import Actor, Movie, Tag, Rating, Rating
# Register your models here.

admin.site.register(Actor)
admin.site.register(Movie)
admin.site.register(Tag)
admin.site.register(Rating)
