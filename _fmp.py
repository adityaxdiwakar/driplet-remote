import json
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
    packet = json.dumps(content)
    ws.send(packet.encode('utf-8'))
    while True:
        command = ws.recv()
        os.system(command)