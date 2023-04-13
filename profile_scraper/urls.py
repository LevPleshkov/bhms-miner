from django.urls import path

from . import views

app_name = 'profile_scraper'
urlpatterns = [
    path('', views.index, name='index'),
]
