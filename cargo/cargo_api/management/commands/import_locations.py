from django.core.management.base import BaseCommand
import pandas

from cargo_api.models import Location


class Command(BaseCommand):
    def handle(self, *args, **options):
        csv_file = "data/uszips.csv"

        # Read the CSV file using pandas
        df = pandas.read_csv(csv_file)

        # Get unique locations
        unique_locations = df[
            ["city", "state_name", "zip", "lat", "lng"]
        ]

        # Create Location objects and save them to the database
        for item, row in unique_locations.iterrows():
            if item == 1000:
                break

            location = Location.objects.create(
                city=row["city"],
                state=row["state_name"],
                mail_index=row["zip"],
                latitude=row["lat"],
                longitude=row["lng"],
            )

        self.stdout.write(self.style.SUCCESS("Locations imported successfully."))
