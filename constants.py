'''
PROTOCOL
legend: 
    CMD => typed out
    tail => typed out 0s
    '|' splits command parts
    B = board size bits
    S = score number bits
    R = row number bits
    C = column number bits
    XX = Tile Type Code
            00 = Blank
            01 = Barrier
            10 = Player
NOTE: most completed commands are 1 byte, but not all. | does NOT split the bytes

SERVER TO CLIENT
    CREATE BOARD    000 | BBBB |0
    MOVE UP         100 | 00000 
    MOVE DOWN       101 | 00000
    MOVE LEFT       101 | 00000
    MOVE RIGHT      111 | 00000
        (of note: all move cmds start w 1...)

CLIENT TO SERVER
    PRINT BOARD     00 | BBBB | 00 
                    then sends encoded string of BBBB**2 length (the board)
    SCORE           01 | SSSS | 00
    DELTA           10 | RRRR | CCCC | XX | 0000
'''


UP      = "U"
DOWN    = "D"
RIGHT   = "R"
LEFT    = "L"

PRINT   = "P"

SHORT           = 1 # num bytes
BYTE_SIZE       = 8
NUMBER_BIT_CT    = 4

# server (recieves)
S_CMD_SIZE      = 3
# S_OPT_SIZE      = BYTE_SIZE - S_CMD_SIZE # option size + tail

S_CREATE_TAIL   = BYTE_SIZE - NUMBER_BIT_CT
S_MOVE_TAIL     = BYTE_SIZE - S_CMD_SIZE

S_SIZE_MASK     = 0b00011110
PRINT_CMD       = 0b00100000

# (to) client
C_CMD_SIZE      = 2
C_PRINT_OPT_SIZE = NUMBER_BIT_CT
C_PRINT_TAIL    = BYTE_SIZE - C_CMD_SIZE - C_PRINT_OPT_SIZE
C_PRINT_OPT_MASK = 0b00111100
# C_PRINT_TAIL_SIZE = 2 

C_SCORE_OPT_SIZE    = 4
C_SCORE_TAIL    = BYTE_SIZE - C_CMD_SIZE - C_SCORE_OPT_SIZE
C_SCORE_MASK    = C_PRINT_OPT_MASK

C_COORD_SIZE    = 4
C_TILETYPE_SIZE = 2
C_ROW_TAIL      = (BYTE_SIZE*2) - C_CMD_SIZE - C_COORD_SIZE
C_COL_TAIL      = C_ROW_TAIL - C_COORD_SIZE
C_DELTA_TAIL    = C_COL_TAIL - C_TILETYPE_SIZE
C_ROW_MASK      = 0b0011110000000000
C_COL_MASK      = 0b0000001111000000


# C_OPT_SMALL     = BYTE_SIZE - C_CMD_SIZE (6)
# C_OPT_LARGE     = BYTE_SIZE*2 - C_CMD_SIZE
C_ROW_TAIL_SIZE = 10
C_COL_TAIL_SIZE = 6

# Commands & Command Fragments
# CREATE_BOARD    = 0b00000000
CREATE_BOARD_MIN    = 0b000
UP_BIN_MIN          = 0b100
DOWN_BIN_MIN        = 0b101
LEFT_BIN_MIN        = 0b110
RIGHT_BIN_MIN       = 0b111
# UP_BIN          = 0b10000000
# DOWN_BIN        = 0b10100000
# LEFT_BIN        = 0b11000000
# RIGHT_BIN       = 0b11100000

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