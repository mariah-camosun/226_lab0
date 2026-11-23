# from django.shortcuts import render
from django.http import HttpResponse
from .models import Player
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

# Create your views here.
def index(request):
    return HttpResponse('Hello world')

def greet( request, name ):
    return HttpResponse(f'Hello {name}')

def greet2( request, fname, lname ):
    return HttpResponse(f'Hello {fname} {lname}')

def get_player(request, player_id):
    players = Player.objects.filter(pk=player_id)
    if len(players) == 1:
        player = players[0]
        return HttpResponse(f'Player {player.tag} is at row {player.row} and col {player.col}')
    else:
        return HttpResponse ('No such player') # should really have an error for >1, b/c should only have one primary key...

def get_all_players(request):
    players = Player.objects.all()
    result=''
    for player in players:
        result += str(player) + '<br>'
    return HttpResponse( result )

def create_player(request, pl_tag, row, col):
    Player.create_player(pl_tag, row, col).save() # adds to db, but doesnt reply! - thats return HttpResponse # NEEDS the .save()

    player = Player.objects.get( tag = pl_tag )
    result = 'player ' + str(player) + ' created' # calls the __str__ func written
    return HttpResponse(result)

def move_player(request, pl_tag, direction):
    player = Player.objects.get(pl_tag = pl_tag)

    match direction:
        case 'up':
            player.row -= 1
        case 'down':
            player.row += 1
        case 'right':
            player.col += 1
        case 'left':
            player.col -= 1
    

class PlayerCreate(CreateView):
    model=Player
    fields='__all__'
    success_url=reverse_lazy('players')

class PlayerUpdate(UpdateView):
    model=Player
    fields=['row','col']
    success_url=reverse_lazy('players')