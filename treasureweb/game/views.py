from django.shortcuts import render
from django.http import HttpResponse
from .models import Tile, Player
# Create your views here.

def welcome(request):
    return HttpResponse("<h3 class='h3' style='text-align: center; margin-top: 50px;'>Welcome! Do you want to be <a href='' >Player One</a> or <a href=''>Player Two</a>?</h3>")

def create_game(self):
    return 

def get_player(request, player_id):
    players = Player.objects.filter(pk=player_id)
    if len(players) == 1:
        player = players[0]
        return HttpResponse( f'Player {player.name} is at row {player.row} and col {player.col}')
    else:
        return HttpResponse( 'No such player')