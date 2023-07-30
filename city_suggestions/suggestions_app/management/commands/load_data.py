
import sys
import csv
import time
from django.core.management.base import BaseCommand
from suggestions_app.models import City

class Command(BaseCommand):
    help = 'Load data from TSV file into the database'
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **kwargs):
        file_path = 'cities_canada-usa.tsv'

        with open(file_path, 'r', encoding='utf-8') as tsvfile:
            reader = csv.DictReader(tsvfile, delimiter='\t')
            csv.field_size_limit(sys.maxsize)
            for row in reader:
                city_name = row['name']
                country = row['country']
                latitude = float(row['lat'])
                longitude = float(row['long'])

                try:
                    city = City(name=city_name, country=country, lat=latitude, lon=longitude)
                    city.save()
                except Exception as e:
                    print(f"Error creating City object for {city_name}: {str(e)}")
