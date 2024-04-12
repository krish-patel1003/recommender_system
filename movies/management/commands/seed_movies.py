from django.core.management.base import BaseCommand
from movies.models import Movie, Tag, Actor
from movies.constants import MoviesConstants
from datetime import datetime
from tqdm import tqdm
import random

class Command(BaseCommand):
    help = 'Adds data to the Movie model using predefined arrays'

    def handle(self, *args, **kwargs):
        # Create tags
        tags = [Tag.objects.get_or_create(name=tag)[0] for tag in MoviesConstants.TAGS]
        
        pbar = tqdm(set(MoviesConstants.MOVIE_NAMES), desc='Adding movies', unit='movie')

        # Add movies
        for name in pbar:
            release_date = datetime(random.randint(1950, 2022), random.randint(1, 12), random.randint(1, 28))
            movie = Movie.objects.create(title=name, release_date=release_date)
            # Add random tags to the movie
            random_tags = random.sample(tags, random.randint(1, 5))
            movie.tags.add(*random_tags)

            # Add random actors to the movie
            actors = Actor.objects.all().order_by('?')[:random.randint(1, 5)]
            movie.actors.add(*actors)

        self.stdout.write(self.style.SUCCESS('Successfully added data to the Movie model'))
