from django.urls import re_path
from metrics.api import MetricsListApiView

app_name = 'metrics'

urlpatterns = [
    re_path('^$', MetricsListApiView.as_view(), name='metrics-list')
]


