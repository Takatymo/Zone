from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'map/$', views.map, name='map'),
    url(r'list/$', views.list, name='list'),
    url(r'places_api/$', views.places_api, name='places_api'),
]