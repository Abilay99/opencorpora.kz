from django.urls import path

from .views import corpora, genres

urlpatterns = [
    path('corpora/', corpora, name='corpora'),
    path('genres/', genres, name='genres')
]