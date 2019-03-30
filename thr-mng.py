import requests
import os
import threading

from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv("CLIENT_ID")
token = os.getenv("ACCESS_TOKEN")

#services = requests.get(f"https://api.driplet.cf/endpoints/{os.getenv("CLIENT_ID")}/services", headers={"authorization": os.getenv("ACCESS_TOKEN")})
services = requests.get(f"http://localhost:3141/endpoints/{client_id}/services", headers={"authorization": token}).json()

import _factory

for service in services:
    threading.Thread(
        target = _factory.service_controller,
        args = [
            service,
            token
        ]
    ).start()