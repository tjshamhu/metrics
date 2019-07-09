from datetime import datetime

from django.contrib.auth.models import User
from django.core.management import call_command
from django.db.models import Sum
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from metrics.models import Metric


class MetricsListAPIViewTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command('load_sample_data')  # import some data into our test db

    def setUp(self):
        super().setUp()
        self.url = reverse('metrics:metrics-list')
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username='jayden',
            email='tjscorp@gmail.com',
            password='jayden'
        )

    def test_unauthenticated_request(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_post_methods_not_available(self):
        self.client.login(username='jayden', password='jayden')
        response = self.client.post(self.url, data={})
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

        response = self.client.patch(self.url, data={})
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

        response = self.client.delete(self.url, data={})
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_ordering(self):
        self.client.login(username='jayden', password='jayden')
        response = self.client.get(self.url + '?ordering=channel')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # test ascending
        data = response.data.get('results', None)
        sorted_data = sorted(data, key=lambda x: x['channel'])
        self.assertListEqual(data, sorted_data)

        # test descending
        response = self.client.get(self.url + '?ordering=-channel')
        data = response.data.get('results', None)
        sorted_data = sorted(data, key=lambda x: x['channel'], reverse=True)
        self.assertListEqual(data, sorted_data)

        # test multiple fields
        response = self.client.get(self.url + '?ordering=country,clicks,spend')
        data = response.data.get('results', None)
        sorted_data = sorted(data, key=lambda x: (x['country'], x['clicks'], x['spend']))
        self.assertListEqual(data, sorted_data)

    def test_filtering(self):
        self.client.login(username='jayden', password='jayden')
        response = self.client.get(self.url + '?os=android')
        data = response.data.get('results', None)
        self.assertTrue(all([entry['os'] == 'android' for entry in data]))

        response = self.client.get(self.url + '?os=android&channel=chartboost')
        data = response.data.get('results', None)
        self.assertTrue(all([entry['os'] == 'android' for entry in data]))
        self.assertTrue(all([entry['channel'] == 'chartboost' for entry in data]))

    def test_grouping(self):
        self.client.login(username='jayden', password='jayden')
        response = self.client.get(self.url + '?grouping=os')
        data = response.data.get('results', None)
        self.assertTrue(len(data) == 2)  # should only be 2 groups, android and ios
        self.assertIn('ios', [entry['os'] for entry in data])
        self.assertIn('android', [entry['os'] for entry in data])

        # test totals after grouping
        aggregation = Metric.objects.filter(os='ios').values('os').aggregate(installs=Sum('installs'))
        ios_installs_total = aggregation['installs']
        ios_data = list(filter(lambda x: x['os'] == 'ios', data))[0]
        self.assertEqual(ios_installs_total, ios_data['installs'])

        # test total after grouping by multiple
        response = self.client.get(self.url + '?grouping=channel,country')
        data = response.data.get('results', None)
        aggregation = Metric.objects.filter(
            channel='google', country='US'
        ).values('channel', 'country').aggregate(spend=Sum('spend'))
        spend_total = aggregation['spend']
        spend_data = list(filter(lambda x: x['channel'] == 'google' and x['country'] == 'US', data))[0]
        self.assertEqual(spend_total, spend_data['spend'])

    def test_scenario_one(self):
        """
        Show the number of impressions and clicks that occurred before the 1st of June 2017,
        broken down by channel and country, sorted by clicks in descending order.
        """
        self.client.login(username='jayden', password='jayden')
        response = self.client.get(self.url + '?date_to=2017-06-01&grouping=channel,country&ordering=-clicks')
        data = response.data.get('results', None)

        # test ordering
        sorted_data = sorted(data, key=lambda x: x['clicks'], reverse=True)
        self.assertListEqual(data, sorted_data)

        # test grouping, clicks totals, adcolony US
        aggregation = Metric.objects.filter(
            date__lte=datetime.strptime('2017-06-01', '%Y-%m-%d'), channel='adcolony', country='US'
        ).values('channel', 'country').aggregate(clicks=Sum('clicks'), impressions=Sum('impressions'))
        clicks_total = aggregation['clicks']
        adcolony_us_data = list(filter(lambda x: x['channel'] == 'adcolony' and x['country'] == 'US', data))[0]
        self.assertEqual(clicks_total, adcolony_us_data['clicks'])
        self.assertEqual(13089, adcolony_us_data['clicks'])  # we know this from the example given

        impressions_total = aggregation['impressions']
        self.assertEqual(impressions_total, adcolony_us_data['impressions'])
        self.assertEqual(532608, adcolony_us_data['impressions'])  # we know this from the example given

        # test grouping, clicks totals, vungle GB
        aggregation = Metric.objects.filter(
            date__lte=datetime.strptime('2017-06-01', '%Y-%m-%d'), channel='vungle', country='GB'
        ).values('channel', 'country').aggregate(clicks=Sum('clicks'), impressions=Sum('impressions'))
        clicks_total = aggregation['clicks']
        vungle_gb_data = list(filter(lambda x: x['channel'] == 'vungle' and x['country'] == 'GB', data))[0]
        self.assertEqual(clicks_total, vungle_gb_data['clicks'])
        self.assertEqual(9430, vungle_gb_data['clicks'])  # we know this from the example given

        impressions_total = aggregation['impressions']
        self.assertEqual(impressions_total, vungle_gb_data['impressions'])
        self.assertEqual(266470, vungle_gb_data['impressions'])  # we know this from the example given
