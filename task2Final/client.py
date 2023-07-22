import requests
import asyncio
import websockets
import json
import sys


def publisher(port, ip):
    payload = {

    }
    response = requests.post(f"http://{ip}:{port}/publisher", json=payload)
    return response.json()



def subscriber(port, ip):
    payload = {

    }
    response = requests.post(f"http://{ip}:{port}/subscriber", json=payload)
    return response.json()
    

# publisher web sockets
async def publisher_websocket(token, port, ip):
    uri = f"ws://{ip}:{port}"
    async with websockets.connect(uri) as websocket:
        request_body = {
            "auth" : token,
            "conf" : 1
        }
        await websocket.send(json.dumps(request_body))




        while True:
            user_input = input("Enter a message ('terminate' to quit): ")
            if (user_input == 'terminate'):
                break
            message_payload = {
                "conf" : 0,
                "message" : user_input,
                "auth" : token
            }
            await websocket.send(json.dumps(message_payload))
            await asyncio.sleep(0)



# subscriber web sockets
async def subscriber_websocket(token, port, ip):
    uri = f"ws://{ip}:{port}"

    async with websockets.connect(uri) as websocket:
        request_body = {
            "auth" : token,
            "conf" : 1
        }
        await websocket.send(json.dumps(request_body))
        while True:
            response = await websocket.recv()
            print("Received:", response)




if (sys.argv[3] == "SUBSCRIBER"):
    token = subscriber(sys.argv[2], sys.argv[1])
    asyncio.run(subscriber_websocket(token, token["socketPort"], sys.argv[1]))
    
elif(sys.argv[3] == "PUBLISHER"):
    token = publisher(sys.argv[2], sys.argv[1])
    asyncio.run(publisher_websocket(token, token["socketPort"], sys.argv[1]))

