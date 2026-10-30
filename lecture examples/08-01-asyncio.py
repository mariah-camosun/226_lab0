# needs a fix somewhere. figure it out
from sys import argv
from asyncio import open_connection, run
from struct import pack

if ( (len(argv) != 3) or (not argv[1].isnumeric()) or (not argv[2].isnumeric()) or (int(argv[1]) > 15) or (int(argv[2]) > 15)):
    print( "Expected 2 coordinates in range [0-15]")

x = int( argv[1] )
y = int( argv[2] )
combined_num = (x << 4) | y
print("xy:", bin(combined_num))

async def send_message(msg):
    reader, writer = await open_connection('127.0.0.1', 34567)
    writer.write( '!B', msg)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

run( send_message(combined_num))