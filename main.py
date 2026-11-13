# #!/usr/bin/python3.11
# from struct import pack, unpack
# from Board import Board
# import constants


# def send_str( socket, string ):
#     #  print( string )
#     #  print( string.encode( 'UTF-8' ) )
#      socket.sendall( string.encode( 'UTF-8' ) ) # Client IP and port implicit due to accept call

# #     return b
   
# def unpack_data( data ):
#     if ( len(data) != constants.SHORT ): 
#         return

#     unpacked_data = unpack( '!B' , data )[0]
#     return unpacked_data
# # def initial_board():
# #     b = Board.new_max_board(10)
# #     show_board_scores(b)
#     # Board(10,5,5)
#     # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#     # while ( b.get_treasure_count() > 0 ):
#     #     print(b)        
#     #     b.report_player_scores()

#     #     players = b.get_players()
#     #     for player in players:
#     #         player.move( )
        
#     # b.report_player_scores()
#     # print("No more treasure to collect!")
#     # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")