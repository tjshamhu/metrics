import django_filters as filters

from metrics.models import Metric


class MetricFilter(filters.FilterSet):
    date_from = filters.DateFilter(method='filter_date_from')
    date_to = filters.DateFilter(method='filter_date_to')

    def filter_date_from(self, queryset, name, value):
        return queryset.filter(date__gte=value)

    def filter_date_to(self, queryset, name, value):
        return queryset.filter(date__lte=value)

    class Meta:
        model = Metric
        fields = {
            'channel': ['exact'],
            'country': ['exact'],
            'os': ['exact'],
            'date': ['exact'],
            'impressions': ['lt', 'gt', 'exact'],
            'clicks': ['lt', 'gt', 'exact'],
            'installs': ['lt', 'gt', 'exact'],
            'spend': ['lt', 'gt', 'exact'],
            'revenue': ['lt', 'gt', 'exact']
        }
