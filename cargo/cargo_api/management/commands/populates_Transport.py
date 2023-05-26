import re

from faker import Faker
from django.core.management import BaseCommand

from cargo_api.models import Location, Transport


def random_unique_id():
    fake = Faker()
    pattern = re.compile(r'\d{4}[A-Z]')
    while True:
        value = f'{fake.random_number(digits=4)}{fake.random_uppercase_letter()}'
        if pattern.match(value):
            unique_id = value
            break
    return unique_id


def random_location():
    location = Location.objects.order_by('?').first()
    return location


class Command(BaseCommand):
    def handle(self, *args, **options):
        for _ in range(20):
            unique_id = random_unique_id()
            location = random_location()

            transport = Transport.objects.create(
                unique_id=unique_id,
                location=location,
            )

        self.stdout.write(self.style.SUCCESS(
            "Transport populated successfully."
        ))

