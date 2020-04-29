import json
import os
import time
import subprocess
import threading

import websocket

def act(service, token):
    content = {
        "user_id": service["associated_to"],
        "auth_token": token,
        "service_id": service["id"]
    }   
    ws = websocket.create_connection("ws://localhost:8000/ws/server")
    ws.send(json.dumps(content))
    command = service["log_command"]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, shell=True)
    # threading.Thread(target=provider, args=[ws, p, content]).start()
    provider(ws, p, service["id"])

def provider(ws, p, service_id):
     while True:
        load = p.stdout.readline()
        payload = {
            "service_id": service_id,
            "log": load.decode('utf-8')
        }
        ws.send(json.dumps(payload))      