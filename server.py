from Board import Board
import constants
import main


#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from struct import pack, unpack
from threading import Thread, current_thread, Semaphore

BUF_SIZE = 1024
HOST = ''
PORT = 12345
SHORT = 1 # num bytes
MIN_PACK_BYTES = 2

def recieve_buffer_data( sc, size ): # recieves data in bitecode format
    data = b''
    while len(data) < size:
        curr_data = sc.recv(size - len(data)) # recvfrom not needed since address known
        if curr_data == b'': #closed connection
            print('closing connection')
            return data
        data += curr_data

    return data

def unpack_data( data ):
    if ( len(data) != SHORT ): 
        return

    unpacked_data = unpack( '!B' , data )[0]
    return unpacked_data

def send_delta( board, isSourse ):
        column, row, prev_content = main.get_tile_details( board )
        print( "row, column:", row, column, "in bin", bin(row), bin(column))
        row = row << 10
        column = column << 6
        if ( isSourse == True ):
            delta = constants.DELTA | row | column | constants.BLANK
            print( bin(delta))
            main.send_cmd( sc, delta, '!H' )
        else:
            delta = constants.DELTA | row | column | constants.PLAYER
            print( bin(delta))
            main.send_cmd( sc, delta, '!H' )

def direct_bin( cmd_byte, board ):
    # print( "Entered direct." )
    # print( "Data in:", cmd_byte, bin(cmd_byte))

    # get cmd portion of split cmd bits from remaining opt bits (via bitshifting)
    cmd = cmd_byte >> ( constants.S_OPT_SIZE )

    if ( cmd == int(constants.CREATE_BOARD) ):
        # opt represents board size, in 4 bits
        opt = ( cmd_byte & constants.S_SIZE_MASK ) # convert cmd bits to 0, using bitmask
        opt = opt >> ( constants.S_OPT_SIZE - constants.OPT_NUM_SIZE ) # cut off trailing 0 not part of opt
        # print( "cmd:",  cmd, bin(cmd), " opt:", opt, bin( opt ) )

        board = Board.new_max_board( opt )
        # print( "boa
        # rd" )
        print( board.__str__() )

        send_board( board.__str__() )
        player = board.get_player( 1 )
        send_score( player.get_score() )

    #otherwise its a move command, direction is one of 4
    else:
        send_delta( board, True )
        player = board.get_player( 1 )

        if ( cmd << ( constants.S_OPT_SIZE ) == (constants.UP_BIN) ):
            player.move( constants.UP )
        elif ( cmd << ( constants.S_OPT_SIZE ) == (constants.DOWN_BIN) ):
            player.move( constants.DOWN )     
        elif ( cmd << ( constants.S_OPT_SIZE ) == (constants.LEFT_BIN) ):
            player.move( constants.LEFT )   
        elif ( (cmd) << ( constants.S_OPT_SIZE ) == (constants.RIGHT_BIN) ):
            player.move( constants.RIGHT )

        send_delta( board, False )
        send_score( player.get_score() )
    main.show_board_scores(board) 
    return board

def send_board( board_str ):
        # pack as unsigned char (1Byte), and send to client
        # board_str = board_str.replace("\n", "").replace(" ", "").split("n", 1)
        board_str = board_str.replace(" ", "").split("n", 1)
        board_str = board_str[0]

        main.send_str( sc, board_str )

def send_score( scoreOpt ):
        # print( "entered send score, score data:", scoreOpt, bin(scoreOpt))
        # scoreOpt = score & 0b001111 # make sure score is only component of cmd that is the 4 bit score sequence
        scoreOpt = scoreOpt << (constants.C_OPT_SMALL - constants.OPT_NUM_SIZE) # add 2 0s at the end to padd to correct position
        fullCmd = (constants.SCORE) | scoreOpt

        # print ( "score data: ", scoreOpt, bin(scoreOpt), "cmd: ", fullCmd, bin(fullCmd), " opt: " )
        main.send_cmd( sc, fullCmd, '!B' )
        main.send_str( sc, '\n' )

with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Details later
    sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
    sock.listen(1) # Server only supports a single 3-way handshake at a time

    print('Server:', sock.getsockname()) # Server IP and port

    board = main.new_board( 10 )
    
    while True:
        sc, _ = sock.accept() # Wait until a connection is established
        # Thread(target=add_to_total, args=(sc,)).start()
        with sc: 
            print('Client:', sc.getpeername()) # Client IP and port
            raw_data = recieve_buffer_data( sc, SHORT )
            data = unpack_data( raw_data )

            print( "recieved (hex):", hex( data ))
            board = direct_bin( data, board )
            # send_data( data )
            # sc.sendall( str(output).encode('utf-8') ) # Client IP and port implicit due to accept call

