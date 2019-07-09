import csv

from django.conf import settings
from django.core.management import BaseCommand

from metrics.models import Metric


class Command(BaseCommand):
    help = 'Load a data from the sample_data.csv file'

    fixture_path = settings.BASE_DIR + 'fixtures/sample_data.csv'

    def handle(self, *args, **kwargs):
        with open(self.fixture_path, 'r') as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader, start=1):
                try:
                    Metric.objects.create(
                        date=row[0],
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

