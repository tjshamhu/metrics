import csv
import os

from datetime import datetime
from django.conf import settings
from django.core.management import BaseCommand

from metrics.models import Metric


class Command(BaseCommand):
    help = 'Load a data from the sample_data.csv file'

    fixture_path = os.path.join(settings.BASE_DIR, 'fixtures', 'sample_data.csv')

    def handle(self, *args, **kwargs):
        print('Beginning import of [{}]'.format(self.fixture_path))

        with open(self.fixture_path, 'r') as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                try:
                    Metric.objects.create(
                        date=datetime.strptime(row[0], '%d.%m.%Y').date(),
                        channel=row[1],
                        country=row[2],
                        os=row[3],
                        impressions=row[4],
                        clicks=row[5],
                        installs=row[6],
                        spend=row[7],
                        revenue=row[8],
                    )
                except Exception as e:
                    print('Failed to import row number [{}].\n {}\n\n'.format(index, e))

