from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('metrics/', include('metrics.urls')),

    # ######################## DOCS #######################
    re_path(r'^docs/', include_docs_urls(title='Metrics API Docs', public=True),),
]
