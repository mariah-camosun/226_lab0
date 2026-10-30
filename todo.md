
# TODO
[~] fix functions that pass in unneccessary variables (eg. Board.Boardsize)
## lab 4
###### Modify main.py so that
    [x] it creates a 10 x 10 board with max barriers and treasures and 
        [x] prints out the board and player score
    [x] it accepts local TCP connections on port 12345
        [x] and non-local 
    [x] it prints out every received byte in hexadecimal form (on server, use hex( num ); not h\00\1e format)
    [x] it implements the protocol shown in the figures on the next page
            [x] if the create board command is received, a board of size x size is created with the maximum number of barriers and treasures, 
                [x] and the entire board string is sent back to the client
            [x] if a motion command is received, 
                [x] the command is passed to the board, and 
                [x] two delta messages are sent back to the client, representing the origin tile's index and value and then the destination tile's index and value; subsequently, 
                [x] the score message is sent
    [ ] after EVERY command is executed, prints
        [ ] the board and 
        [ ] score
    [~] it ignores incoming messages that do not comply with the protocol
    [x] it closes the connection after every message
    [x] it is refactored to use functions throughout
    [x] it does not crash
## lab 5
### stage 1:
#### client to do: 
    [ ] connect to server
    [ ] send print cmd to server
        [ ] update server to accept print cmd
    [ ] close connection
    [ ] print board
    then repeatedly:
        [ ] prompt for cmd - one of: print, up, down, left, right
        [ ] print updated board
        [ ] print score from server
#### once client 'done':
    [ ] make sure all tests still pass
    [ ] conf w another student servers and clients compatible
    [ ] commit/push - DONT merge to main

### stage 2:
#### update server:
    [ ] support 2 players (2 chars on board, 2 scores)
    [ ] maintain *at least* 1 thread per connection
            may need more threads to communicate w clients
    [ ] accept only first 2 connections
        [ ] close further connections immediately
    [ ] maintain 1 thread to access board
            no other thread may access the board
            no global variables may be used EXCEPT: input_queue, output_queue (facillitate communication btwn board & other threads)
#### update client support:
    [ ] being p1 or p2
    [ ] print out board deltas, 
        [ ] incl other player's
    [ ] implement protocol described in lab 5, p 25
## finish:
    [ ] commit/push
    [ ] merge w main
    [ ] demo

note: for this lab, assume python sockets are thread safe - only true b/c using threading library