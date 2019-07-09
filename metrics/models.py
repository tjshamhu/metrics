from django.db import models


class Metric(models.Model):
    date = models.DateField()
    channel = models.CharField(max_length=50)
    country = models.CharField(max_length=2)
    os = models.CharField(max_length=10)
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    installs = models.IntegerField()
    spend = models.IntegerField()
    revenue = models.FloatField()
