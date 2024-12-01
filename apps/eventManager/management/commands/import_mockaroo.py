import csv
from django.core.management.base import BaseCommand
from apps.eventManager.models import Stadium

class Command(BaseCommand):
    help = 'Import mock data from Mockaroo'

    def handle(self, *args, **kwargs):
        file_path = '/home/shio/Downloads/MOCK_DATA.csv'  # Update this path
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Stadium.objects.create(
                    id=row['id'],
                    name=row['name'],
                    address=row['address'],
                    capacity=row['capacity'],
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported mock data!'))
