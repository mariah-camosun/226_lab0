from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('greet/<str:name>/', views.greet, name='greet'),
    path('greet2/<str:fname>/<str:lname>/', views.greet2, name='greet2'),
    path('player/<str:player_id>/', views.get_player, name='player'),
    path('player/', views.get_all_players, name='players'),
    path('player/create/', views.PlayerCreate.as_view(), name='player_create'),
    path('player/update/<int:pk>/', views.PlayerUpdate.as_view(), name='player_update'),
    path('player/create/<str:pl_tag>/<int:row>/<int:col>/', views.create_player, name='create_player'),
]

# BECOMES PICKY about the trailing slash or not