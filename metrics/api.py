from django.db.models import Sum, DecimalField, F, ExpressionWrapper
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from metrics.filters import MetricFilter
from metrics.models import Metric
from metrics.serializers import MetricSerializer, GroupedMetricSerializer


class MetricsListApiView(ListAPIView):
    serializer_class = MetricSerializer
    model = Metric
    permission_classes = [IsAuthenticated, ]
    filterset_class = MetricFilter
    ordering_fields = ('channel', 'country', 'os', 'date', 'impressions', 'clicks', 'installs', 'spend', 'revenue',
                       'cpi')

    def get(self, request, *args, **kwargs):
        grouping = self.get_grouping()
        if not grouping:
            return super().get(request, *args, **kwargs)

        _filter = MetricFilter(self.request.GET, queryset=self.get_queryset())
        queryset = _filter.qs

        qs = queryset.values(*grouping).annotate(
            Sum('impressions'),
            Sum('clicks'),
            Sum('installs'),
            Sum('spend'),
            Sum('revenue'),
            cpi=ExpressionWrapper(
                F('spend__sum') / F('installs__sum'),
                output_field=DecimalField(decimal_places=2, max_digits=20)
            )
        )

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def get_serializer_class(self):
        grouping = self.get_grouping()
        return GroupedMetricSerializer if grouping else MetricSerializer

    def get_queryset(self):
        queryset = self.model.objects.annotate(
            cpi=ExpressionWrapper(
                F('spend') / F('installs'),
                output_field=DecimalField(decimal_places=2)
            )
        )
        return queryset

    def get_grouping(self):
        params = self.request.query_params.get('grouping', None)
        if params:
            query_fields = [param.strip() for param in params.split(',')]
            model_fields = [field.name for field in self.model._meta.get_fields()]
            grouping = (field for field in query_fields if field in model_fields)
            if grouping:
                return list(grouping)
        return None
