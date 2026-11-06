#!/usr/bin/python3.11
from struct import pack, unpack
from Board import Board
import constants



# def send_cmd( socket, number, format_flag ):
#     # sc.sendall( pack( '!B', number) ) # Client IP and port implicit due to accept call
#     socket.sendall( pack( format_flag, number) ) # Client IP and port implicit due to accept call

def send_str( socket, string ):
    #  print( string )
    #  print( string.encode( 'UTF-8' ) )
     socket.sendall( string.encode( 'UTF-8' ) ) # Client IP and port implicit due to accept call

def get_tile_details( board ):
        active_player = board.get_player(1)
        column, row = active_player.get_coords()
        tile_contains = board.get_coord_tile( column, row ).get_contents()
        print( "getTileDetails: col, row", column, row)

        return column, row, tile_contains

def show_board_scores(b):
    print( b )
    print( b.report_player_scores() )

def new_board( num ):
    b = Board.new_max_board(num)
    show_board_scores(b)
    return b
   
def unpack_data( data ):
    if ( len(data) != constants.SHORT ): 
        return

    unpacked_data = unpack( '!B' , data )[0]
    return unpacked_data
# def initial_board():
#     b = Board.new_max_board(10)
#     show_board_scores(b)
    # Board(10,5,5)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # while ( b.get_treasure_count() > 0 ):
    #     print(b)        
    #     b.report_player_scores()

    #     players = b.get_players()
    #     for player in players:
    #         player.move( )
        
    # b.report_player_scores()
    # print("No more treasure to collect!")
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")