from asyncio import run, start_server, StreamReader, StreamWriter
from struct import pack, unpack

async def process_request( reader: StreamReader, writer: StreamWriter):
    # because server repeatedly...
    while True: 
        try:
            # read in a byte
            data = await reader.read(1)
            if data == b'':
                # break
                return
            else:
                print( "data:", data)
                # (if number unpack, if string decode)
                udata = unpack( '!B', data)[0]
                # do bit manipulation
                op = udata >> 6
                num1 = ( udata & 0b00111000 ) >> 3
                num2 = udata & 0b00000111
                print( op, num1, num2 )
                # preform operations
                if op == 0: #addition
                    result = num1 + num2
                elif op == 1:
                    result = num1 - num2
                elif op == 2:
                    result = num1 * num2
                elif op == 3:
                    result = num1 // num2
                print( "=", result )

                # semd
                writer.write( pack( '!Q', result ) )
                await writer.drain()
        except Exception as e:
            print(e)

        writer.close()
        await writer.wait_closed()
    

async def main():
    server = await start_server( process_request, '', 12346)
    await server.serve_forever()

run( main() )