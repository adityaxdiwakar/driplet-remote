import json
import os
import time
import threading

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
    threading.Thread(target=run_commands, args=[ws]).start()
    pinger(ws)

def pinger(ws):
    while True:
        ws.send("Ping")
        time.sleep(1)

def run_commands(ws):
    while True:
        command = ws.recv()
        os.system(command)