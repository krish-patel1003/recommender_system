from django.core.management.base import BaseCommand
from authentication.models import CustomUser, CustomUserManager
from faker import Faker
import tqdm


class Command(BaseCommand):

    help = "Seed users in the database"

    def handle(self, *args, **options):
        fake = Faker()
        for _ in tqdm.tqdm(range(20)):
            username = fake.user_name()
            password = fake.password()

            CustomUser.objects.create_user(username=username, password=password)
        self.stdout.write(self.style.SUCCESS(f"User {username} created successfully"))
            
        

