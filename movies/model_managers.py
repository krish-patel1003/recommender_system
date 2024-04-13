from typing import Any
from django.core.cache import cache
from django.db import models


class MovieQuerySet(models.QuerySet):

    def all(self):
        cache_key = 'all_movies'
        movies = cache.get(cache_key)

        if movies is None:
            print("Fetching from DB")
            movies = list(super().all())
            cache.set(cache_key, movies, timeout=60*60*24)
        
        return movies
    

class MovieModelManager(models.Manager):
    
    def get_queryset(self):
        return MovieQuerySet(self.model, using=self._db)
        
        
class RatingsQuerySet(models.QuerySet):

    def all(self):
        cache_key = 'all_ratings'
        ratings = cache.get(cache_key)

        if ratings is None:
            ratings = list(super().all())
            cache.set(cache_key, ratings, timeout=60*60*24)
        
        return ratings
    

    def filter_by_user(self, user: Any):
        cache_key = f'ratings_{user.username}'
        ratings = cache.get(cache_key)

        if ratings is None:
            ratings = list(super().filter(user=user))
            cache.set(cache_key, ratings, timeout=60*60*24)
        
        return ratings
    

class RatingsModelManager(models.Manager):
    
    def get_queryset(self):
        return RatingsQuerySet(self.model, using=self._db)
    
    def filter_by_user(self, user: Any):
        return self.get_queryset().filter_by_user(user)