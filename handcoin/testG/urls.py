from django.urls import path
from . import views

# 게임 path 추가

urlpatterns = [
    path("", views.main, name='main'),
    path("play/<str:title>", views.play, name='play'),
    path("snake", views.snake, name='snake'),
    path("plane", views.plane, name='plane'),
    path("bricksbreak", views.bricksbreak, name='bricksbreak'),
    path("tetris", views.tetris, name='tetris'),
    path("packman", views.packman, name='packman'),
]
