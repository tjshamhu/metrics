from django.db import models


class Metric(models.Model):
    date = models.DateField()
    channel = models.CharField(max_length=50)
    country = models.CharField(max_length=2)
    os = models.CharField(max_length=10)
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    installs = models.IntegerField()
    spend = models.DecimalField(decimal_places=1, max_digits=8)
    revenue = models.DecimalField(decimal_places=2, max_digits=8)
