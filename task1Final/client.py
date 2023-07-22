import requests
import asyncio
import websockets
import json
import sys



# subscriber web sockets
async def subscriber_websocket(port, ip):
    uri = f"ws://{ip}:{port}"

    async with websockets.connect(uri) as websocket:
        while True:
            user_input = input("Enter a message ('terminate' to quit): ")
            if (user_input == 'terminate'):
                exit(0)
            message_body = {
                "message": user_input
            }
            await websocket.send(json.dumps(message_body))
            await asyncio.sleep(0)
        
        





asyncio.run(subscriber_websocket(sys.argv[2], sys.argv[1] ))
