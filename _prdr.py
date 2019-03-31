import json
import os
import time
import subprocess
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
            "content": "",
            "type": "Log Provider"
        }
    }   
    ws = create_connection("wss://private-ws.driplet.cf")
    command = service["log_command"]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, shell=True)
    threading.Thread(target=provider, args=[ws, p, content]).start()
    pinger(ws)                                         

def pinger(ws):
    while True:
        ws.send("Ping")
        time.sleep(1)

def provider(ws, p, content):
     while True:
        load = p.stdout.readline()
        content["payload"]["content"] = load.decode('utf-8')
        ws.send(json.dumps(content))      