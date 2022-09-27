from django.urls import path
from django.shortcuts import render

from . import views as crosswords

app_name = 'crosswords'


def default(request):
    return render(request, "crosswords/{}.html".format(request.resolver_match.url_name))


urlpatterns = [
    path('', default, name='index'),
    path('about/', default, name='about'),
    path('rules/', default, name='rules'),

    path('design/', crosswords.play, name='design'),
    path('play/', crosswords.play, name='play'),
    path('pdf/', crosswords.pdf, name='pdf'),
]
