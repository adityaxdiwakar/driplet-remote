import os

from websocket import create_connection

def act(service, token):
    content = {
        "credentials": {
            "client_id": service["associated_to"],
            "token": token
        }, 
        "payload": {
            "service_id": service["id"],
            "type": "Action Polling"
        }
    }
    ws = create_connection("wss://private-ws.driplet.cf")
    while True:
        command = ws.recv()
        os.system(command)
        