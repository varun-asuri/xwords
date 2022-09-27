from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Crosswords Database Administration"

urlpatterns = [
    path('', include('xwords.apps.crosswords.urls', namespace='crosswords')),
    path('api/', include('xwords.apps.api.urls', namespace='api')),
    path('admin/', admin.site.urls),
]
