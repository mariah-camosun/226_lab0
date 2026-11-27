from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='index'),
    # path('game/new/', views.create_game, name='create_game'),
    path('player/', views.get_all_players, name='players'),
    path('player/<int:player_id>/', views.get_player, name='player'),
    path('player/create/', views.CreatePlayer.as_view(), name='player_create'),
    path('player/create/<str:name>/<int:row>/<int:col>/', views.create_player_at, name='player_create'),
    path('player/update/<int:player_id>/', views.UpdatePlayer.as_view(), name='player_update'),
]