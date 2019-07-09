from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from metrics.models import Metric
from metrics.serializers import MetricSerializer


class MetricsListApiView(ListAPIView):
    serializer_class = MetricSerializer
    model = Metric
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return self.model.objects.all()
