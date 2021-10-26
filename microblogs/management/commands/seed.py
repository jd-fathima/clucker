from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from microblogs.models import User


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        for x in range(100):
            newUserFirstName = self.faker.first_name()
            newUserLastName = self.faker.last_name()
            newUserEmail = newUserFirstName + newUserLastName + '@example.org'
            newUserUsername = '@'+newUserFirstName +newUserLastName
            newUserBio = self.faker.text()
            newUserPassword = self.faker.password()
            self.user = User.objects.create_user(
                newUserUsername,
                first_name = newUserFirstName,
                last_name = newUserLastName,
                email = newUserEmail,
                bio = newUserBio,
                password = newUserPassword
            )
