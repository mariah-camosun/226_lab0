from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
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

def get_all_players(request):
    players = Player.objects.all()
    result = ''
    for player in players:
        result += str(player) + '<br>'
    return HttpResponse(result)

def create_player_at(self, name, row, col ):
    players = Player.objects.filter(name=name)
    if (players):
        return HttpResponse( 'Player already Exists')
    else:
        Player.create_player_at(name, row, col).save()
        player = ( Player.objects.filter(name=name) )[0]
        return HttpResponse( f'Player {player.name} created at row {player.row}, col {player.col} <br> score = {player.score}')

class CreatePlayer(CreateView):
    model = Player
    fields = '__all__'
    success_url = reverse_lazy('players')

class UpdatePlayer(UpdateView):
    model = Player
    fields = ['row', 'col', 'score']
    success_url = reverse_lazy('players')

