from django.core.management.base import BaseCommand
from movies.models import Actor
from faker import Faker
import tqdm


class Command(BaseCommand):

    help = "Seed users in the database"

    def handle(self, *args, **options):
        fake = Faker()
        for _ in tqdm.tqdm(range(100)):
            name = fake.name()
            age = fake.random_int(min=18, max=60)

            Actor.objects.create(name=name, age=age)
        self.stdout.write(self.style.SUCCESS(f"Actors created successfully"))

            
            
            
        

