from websocket import create_connection
import json
import subprocess
import threading

import _fmp

def service_controller(service, token):
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
    thr = threading.Thread(target=_fmp.act, args=[service, token])
    ws = create_connection("wss://private-ws.driplet.cf")
    command = service["log_command"]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, shell=True)
    while True:
        load = p.stdout.readline()
        content["payload"]["content"] = load.decode('utf-8')
        ws.send(json.dumps(content)) 