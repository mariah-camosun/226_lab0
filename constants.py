'''
PROTOCOL
legend: 
    CMD => typed out
    tail => typed out 0s
    '|' splits command parts
    B = board size bits
    S = score number bits (p1)
    s = score number bits (p2)
    R = row number bits
    C = column number bits
    XX = Tile Type Code
            00 = Blank
            01 = Barrier
            10 = Player 1
            11 = Player 2'''
#    PPPP = Player
#           0000 = Player 1
#           0001 = Player 2
#   __ = Move Direction (below)
'''NOTE: ' | ' does NOT split the bytes

CLIENT TO SERVER
    CREATE BOARD    000 | BBBB |0'''

#   MOVE            1__ | PPPP | 0
''' MOVE UP         _00 | PPPP | 0
    MOVE DOWN       _01 | PPPP | 0
    MOVE LEFT       _01 | PPPP | 0
    MOVE RIGHT      _11 | PPPP | 0
        (of note: all move cmds start w 1...)

SERVER TO CLIENT
    PRINT BOARD     00 | BBBB | 00 
          then sends encoded string of BBBB**2 length (the board)'''
#    SCORE           01 | SSSS | ssss | 000000
#    DELTA           10 | RRRR | CCCC | XX | 0000


UP      = "U"
DOWN    = "D"
RIGHT   = "R"
LEFT    = "L"

PRINT   = "P"

SHORT           = 1 # num bytes
BYTE_SIZE       = 8
NUMBER_BIT_CT    = 4

# CLIENT SENDS 
C_CMD_SIZE      = 3

C_CREATE_TAIL   = BYTE_SIZE - NUMBER_BIT_CT
C_MOVE_TAIL     = BYTE_SIZE - C_CMD_SIZE

C_SIZE_MASK     = 0b00011110

# SERVER SENDS
S_CMD_SIZE      = 2
S_PRINT_OPT_SIZE = NUMBER_BIT_CT
S_PRINT_TAIL    = BYTE_SIZE - S_CMD_SIZE - S_PRINT_OPT_SIZE
S_PRINT_OPT_MASK = 0b00111100

S_SCORE_OPT_SIZE    = 4
S_SCORE_TAIL    = BYTE_SIZE - S_CMD_SIZE - S_SCORE_OPT_SIZE
S_SCORE_MASK    = S_PRINT_OPT_MASK

S_COORD_SIZE    = 4
S_TILETYPE_SIZE = 2
S_ROW_TAIL      = (BYTE_SIZE*2) - S_CMD_SIZE - S_COORD_SIZE
S_COL_TAIL      = S_ROW_TAIL - S_COORD_SIZE
S_DELTA_TAIL    = S_COL_TAIL - S_TILETYPE_SIZE
S_ROW_MASK      = 0b0011110000000000
S_COL_MASK      = 0b0000001111000000

S_ROW_TAIL_SIZE = 10
S_COL_TAIL_SIZE = 6

# Commands & Command Fragments
# FROM CLIENT
C_PRINT_CMD       = 0b00100000
CREATE_BOARD_MIN    = 0b000
UP_BIN_MIN          = 0b100
DOWN_BIN_MIN        = 0b101
LEFT_BIN_MIN        = 0b110
RIGHT_BIN_MIN       = 0b111

# FROM SERVER
PRINT_BOARD     = 0b00000000
SCORE           = 0b01000000
DELTA           = 0b1000000000000000

PRINT_BOARD_CMD = 0b00
SCORE_CMD       = 0b01
DELTA_CMD       = 0b10

TILE_MASK       = 0b110000
# BLANK_2         = 0b00
# BARRIER_2       = 0b01
# PLAYER_2        = 0b10

BLANK           = 0b000000
BARRIER         = 0b010000
PLAYER          = 0b100000

REG_PACK_FLAG  = '!B'
LONG_PACK_FLAG  = '!H'