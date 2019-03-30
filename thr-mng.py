import _factory
import requests
import os
import threading
import multiprocessing as mp
import time

from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv("CLIENT_ID")
token = os.getenv("ACCESS_TOKEN")

# services = requests.get(f"https://api.driplet.cf/endpoints/{os.getenv("CLIENT_ID")}/services", headers={"authorization": os.getenv("ACCESS_TOKEN")})
services = requests.get(
    f"https://api.driplet.cf/endpoints/{client_id}/services", headers={"authorization": token}).json()


for service in services:
    service.pop('logs')

sd = {}
for service in services:
    ip = mp.Process(
        target=_factory.service_controller,
        args=[
            service,
            token
        ]
    )
    ip.start()
    sd.update({service["id"]: ip})

while True:
    nc = requests.get(
        f"https://api.driplet.cf/endpoints/{client_id}/services", headers={"authorization": token}).json()
    
    for service in nc:
        service.pop('logs')
    
    if nc != services:
        for service in nc:
            if service not in services:
                # new service
                ip = mp.Process(
                    target=_factory.service_controller,
                    args=[
                        service,
                        token
                    ]
                )
                ip.start()
                sd.update({service["id"]: ip})
        for service in services:
                if service not in nc:
                    # deleted service
                    sd[service["id"]].terminate()
        services = nc
    time.sleep(15)