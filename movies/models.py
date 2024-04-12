from django.db import models
from django.conf import settings

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

    def __str__(self):
        return self.title
    

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])

    def __str__(self):
        return f'{self.user.username} rated {self.movie.title} {self.rating}/5'