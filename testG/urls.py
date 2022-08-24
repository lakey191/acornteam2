from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name='main'),
    path("play/<str:title>", views.play, name='play'),
    path("snake", views.snake, name='snake'),
    path("plane", views.plane, name='plane'),
]
