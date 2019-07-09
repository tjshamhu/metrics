from rest_framework import serializers

from metrics.models import Metric


class MetricSerializer(serializers.ModelSerializer):
    cpi = serializers.DecimalField(decimal_places=3, max_digits=20)

    class Meta:
        model = Metric
        fields = '__all__'


class GroupedMetricSerializer(MetricSerializer):

    def to_representation(self, instance):
        return instance
