from django.core.management.base import BaseCommand
from movies.models import Movie, Rating
from authentication.models import CustomUser
from movies.constants import MoviesConstants
from datetime import datetime
from tqdm import tqdm
import random

class Command(BaseCommand):
    help = 'Adds data to the Rating model using random ratings for each movie and user'

    def handle(self, *args, **kwargs):
        # Get all users
        users = CustomUser.objects.all()
        pbar_users = tqdm(users, desc='Generating User ratings', unit='user')

        # Get all movies
        movies = Movie.objects.all()

        num_movies = movies.count()
        min_items_rated = num_movies // 2

        user_ratings = {}

        for user in pbar_users:
            num_rated_movies = random.randint(min_items_rated, num_movies)
            rated_movies = random.sample(list(movies.values_list("id", flat=True).distinct()), num_rated_movies)
            user_ratings[user.id] = {f"{movie}": random.randint(1, 5) for movie in rated_movies}

        pbar_ratings = tqdm(user_ratings.keys(), desc='Add user ratings', unit='ratings')

        for user_id in pbar_ratings:
            for movie_id, rating in user_ratings[user_id].items():
                rating = Rating.objects.create(
                    rating=rating,
                    movie_id=movie_id,
                    user_id=user_id
                )

        self.stdout.write(self.style.SUCCESS('Successfully added data to the Rating model'))
