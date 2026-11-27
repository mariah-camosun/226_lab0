from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='index'),
    # path('game/new/', views.create_game, name='create_game'),
    path('player/<int:player_id>/', views.get_player, name='player'),
]