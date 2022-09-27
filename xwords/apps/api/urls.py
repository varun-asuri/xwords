from django.urls import path

from . import views as api

app_name = 'api'

urlpatterns = [
    path('create/', api.create, name='create'),
    path('cache/', api.cache, name='cache'),
]
