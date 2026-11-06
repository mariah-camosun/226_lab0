UP      = "U"
DOWN    = "D"
RIGHT   = "R"
LEFT    = "L"

PRINT   = "P"

SHORT           = 1 # num bytes
BYTE_SIZE       = 8
OPT_NUM_SIZE    = 4

# server (recieves)
S_CMD_SIZE      = 3
S_OPT_SIZE      = BYTE_SIZE - S_CMD_SIZE
S_SIZE_MASK     = 0b00011110
PRINT_CMD       = 0b00100000

# (to) client
C_CMD_SIZE      = 2
C_OPT_SMALL     = BYTE_SIZE - C_CMD_SIZE
C_OPT_LARGE     = BYTE_SIZE*2 - C_CMD_SIZE
C_SIZE_MASK     = 0b00111100

# Commands & Command Fragments
CREATE_BOARD    = 0b00000000
UP_BIN          = 0b10000000
DOWN_BIN        = 0b10100000
LEFT_BIN        = 0b11000000
RIGHT_BIN       = 0b11100000

SEND_BOARD      = 0b00000000
SCORE           = 0b01000000
DELTA           = 0b1000000000000000

BLANK           = 0b000000
BARRIER         = 0b010000
PLAYER          = 0b100000

REG_PACK_FLAG  = '!B'
LONG_PACK_FLAG  = '!H'