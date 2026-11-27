from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .cls import Board, Player
from .models import Tile, Player
from .cls import Tile
# Create your views here.

def welcome(request):
    return HttpResponse("<h3 class='h3' style='text-align: center; margin-top: 50px;'>Welcome! Do you want to be <a href='' >Player One</a> or <a href=''>Player Two</a>?</h3>")

def get_player(request, player_id):
    players = Player.objects.filter(pk=player_id)
    if len(players) == 1:
        player = players[0]
        return HttpResponse( f'Player {player.name} is at row {player.row} and col {player.col}')
    else:
        return HttpResponse( 'No such player')

def get_all_players():
    return Player.objects.all()

def update_player_position(player, row, col, score):
    player.row = row
    player.col = col
    player.save()
    return player

def update_player_score(player, score):
    player.score = score
    player.save()
    return player

def get_all_players(request):
    players = get_all_players()
    result = ''
    for player in players:
        result += str(player) + '<br>'
    return HttpResponse(result)

def create_or_update_player_at(name, row, col):
    players = Player.objects.filter(name=name)
    if (players and players.len()==0):
        update_player_position(players[0], row, col)
        return True
    elif (players):
        return False
    else:
        Player.create_player_at(name, row, col).save()
        player = ( Player.objects.filter(name=name) )[0]
        return True

def create_player_at(request, name, row, col):
    if create_or_update_player_at(name, row, col):
        return HttpResponse( f'Player {player.name} created at row {player.row}, col {player.col} <br> score = {player.score}')
    else:
        return HttpResponse( 'Problem Finding Player' )


def create_game(self):
    board = Board.Board(10, 5, 4)
    players = board.get_players()
    p1 = players[0]
    p2 = players[1]
    board_str = str(board)
    board_str += "<br>"
    board_str += "Player 1 Score " + (str)(p1.get_score())
    board_str += "<br>"
    board_str += "Player 2 Score " + (str)(p2.get_score())
    create_player_at( "One", p1.get_name(), p1.get_coords()[0], p1.get_coords()[1] )
    create_player_at( "Two", p2.get_name(), p2.get_coords()[0], p2.get_coords()[1] )
    output = "<div style='align-content: center; height: 100vh;'><h4 class='h4' style='text-align: center; margin-top: -4em;'>New game started!</h4>"
    # output += "<br>"
    output += "<p style='font-family: monospace; text-align: center; margin-top: 30px;'>"
    output += board_str
    output += "</p></div>"
    return HttpResponse( output )

def get_board():
    board = Board.objects.all()
    if board.len() > 1:
        return HttpResponse( 'Problem Retrieving Gameboard')
    else:
        return board

def join_game(self):
    board = get_board()
    players = get_all_players()
    p1 = players[0]
    p2 = players[1]
    board_str = str(board)
    board_str += "<br>"
    board_str += "Player 1 Score " + (str)(p1.get_score())
    board_str += "<br>"
    board_str += "Player 2 Score " + (str)(p2.get_score())
    output = f"<div style='align-content: center; height: 100vh;'><h4 class='h4' style='text-align: center; margin-top: -4em;'>Player {player.name}</h4>"
    # output += "<br>"
    output += "<p style='font-family: monospace; text-align: center; margin-top: 30px;'>"
    output += board_str
    output += "</p>"
    output += "<button type='button'>&UPWARDSARROW</button>"
    output += "</div>"
    return HttpResponse( output )

def play_game_as(self):
    pass

class UpdatePlayer(UpdateView):
    model = Player
    fields = ['row', 'col', 'score']
    success_url = reverse_lazy('players')

