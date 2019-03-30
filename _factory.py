from websocket import create_connection
import json
import subprocess

def service_controller(service, token):
    content = {
        "credentials": {
            "client_id": service["associated_to"],
            "token": token
        },
        "payload": {
            "service_id": service["id"],
            "content": ""
        }
    }
    ws = create_connection("ws://127.0.0.1:3143/")
    command = service["log_command"]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, shell=True)
    while True:
        load = p.stdout.readline()
        content["payload"]["content"] = load.decode('utf-8')
        ws.send(json.dumps(content)) 
