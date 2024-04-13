from django.db import models
from django.conf import settings
from movies.model_managers import MovieModelManager, RatingsModelManager
from django.core.cache import cache 

# Create your models here.
class Actor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100, unique=True)
    release_date = models.DateField()
    actors = models.ManyToManyField(Actor)
    tags = models.ManyToManyField(Tag)

    objects = MovieModelManager()

    def __str__(self):
        return self.title
    
    def get_tags(self):
        return ', '.join([tag.name for tag in self.tags.all()])
    
    def get_actors(self):
        return ', '.join([actor.name for actor in self.actors.all()])
    
    def get_rating(self):
        return self.rating_set.aggregate(models.Avg('rating'))['rating__avg']
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Clear cache
        cache.delete('all_movies')
    

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])

    objects = RatingsModelManager()

    def __str__(self):
        return f'{self.user.username} rated {self.movie.title} {self.rating}/5'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Clear cache
        cache.delete('all_ratings')
        cache.delete(f'ratings_{self.user.username}')
        cache.delete('matrix')
        cache.delete('neighbors')