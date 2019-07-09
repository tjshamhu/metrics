from django.urls import re_path
from metrics.api import MetricsListApiView

app_name = 'artists'

urlpatterns = [
    re_path('^metrics/$', MetricsListApiView.as_view(), name='metrics-list')
]


